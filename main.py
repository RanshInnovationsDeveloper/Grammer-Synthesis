
# Importing necessary libraries
import re
import string
import requests
import nltk
nltk.download('punkt')
from difflib import SequenceMatcher
from IPython.display import HTML
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from spellchecker import SpellChecker

from flask import Flask, request, jsonify
app = Flask(__name__)

## Model for correcting grammar
grammar_pipeline = pipeline("text2text-generation", model="MOKSHm/t5-base-grammar-synthesis")
## Model for paraphrasing
paraphrasing_tokenizer = AutoTokenizer.from_pretrained("humarin/chatgpt_paraphraser_on_T5_base")
paraphraser_model = AutoModelForSeq2SeqLM.from_pretrained("humarin/chatgpt_paraphraser_on_T5_base")

def comparison_highlight(sen1, sen2):
    matcher = SequenceMatcher(None, sen1, sen2)
    opcodes = matcher.get_opcodes()
    highlighted = []
    for tag, i1, i2, j1, j2 in opcodes:
        if tag == 'equal':
            highlighted.append(sen2[j1:j2])
        else:
            highlighted.append(f'[<font color="red"><b>{sen1[i1:i2]}</b></font>]<font color="green"><b>{sen2[j1:j2]}</b></font>')
    return ''.join(highlighted)


# Function that will highlight changes on final grammatically corrected text
def underline_grammar_errors(original_text, corrected_text):
    # Tokenize the original and corrected texts
    original_tokens = nltk.word_tokenize(original_text)
    corrected_tokens = nltk.word_tokenize(corrected_text)

    # Initialize an empty list to store the highlighted tokens
    highlighted_tokens = []

    # Iterate through the corrected tokens
    for i, token in enumerate(corrected_tokens):
        lowercase_token = token.lower()
        # Check if the token exists in the original text (case-insensitive)
        if lowercase_token in [t.lower() for t in original_tokens]:
            highlighted_tokens.append(token)
        else:
            # Handle space for certain tokens
            if token in ["n't", "'s", "'re", "'m", "'ll", ",", ".", "?", "!", ";", ":"]:
                highlighted_tokens[-1] += f'<mark>{token} </mark>'
            else:
                highlighted_tokens.append(f'<mark>{token}</mark>')

    result = ""
    for i, word in enumerate(highlighted_tokens):
        # Add special tokens without space
        if word in ["n't", "'s", "'re", "'m", "'ll", ",", ".", "?", "!", ";", ":"]:
            result += word
        # Add other tokens with a space
        else:
            result += " " + word

    # Remove leading/trailing spaces and return the result
    result = result.strip()
    return result

def is_valid_word(word):
    api_key = "48a89ac5-75c0-46a4-9696-e0a7df3647a6"
    base_url = "https://www.dictionaryapi.com/api/v3/references/collegiate/json/"

    response = requests.get(base_url + word, params={"key": api_key})
    if response.status_code == 200:
        definitions = response.json()
        if "meta" in definitions[0]:
            return True
    return False

# Function to handle any possible spelling error if still there in grammared text
def possible_spellcorr(text):
    # Create a SpellChecker instance for spell checking
    spell = SpellChecker()
    # Initialize an empty list to store the corrected words or tokens
    corrected_words = []

    # Tokenize the text, preserving punctuation, contractions, and other tokens
    tokens = re.findall(r"'s|'t|'re|'ll|'m|[\w]+|[.,!?;:]", text)

    for i, token in enumerate(tokens):
        # Check if the token is a word
        if re.match(r"[\w]+", token):
            # We are first checking the validity of a word using pyspellchecker library
            if token != "'t" and not spell.correction(token) == token:
                # We are checking the word that pyspellchecker thinks is invalid using "Merriam Webster dictionary API"(the reason is given above)
                if not is_valid_word(token):
                    corrected_word = spell.correction(token)
                    if corrected_word is not None:
                        corrected_words.append(corrected_word)
                    else:
                        corrected_words.append(token)
                else:
                    corrected_words.append(token)
            else:
                    corrected_words.append(token)
        else:
          # Token is punctuation or a contraction, handle accordingly
            if i > 0:
                corrected_words[-1] += token
            else:
                corrected_words.append(token)

    corrected_text = ' '.join(corrected_words)
    return corrected_text

# Function that will return text after correcting the grammar
def correcting_grammar(text):
    # Split the text into sentences using NLTK
    sentences = nltk.sent_tokenize(text)

    # Initialize a list to store corrected sentences and highlighted sentences
    corrected_sentences = []
    comparison_sentences = []
    underlined_sentences = []

    # If paragraph, process each sentence individually
    for sentence in sentences:
        if len(sentence) <= 2:
#             print(sentence)
            pass
        else:
            correction = grammar_pipeline("grammar: "+ sentence)
            # Grammaticaly correct sentence
            corrected_text = possible_spellcorr(str(correction[0]['generated_text']))

            # Getting the comparison text that shows what is deleted(using red inside []) and what is added(using green)
            comparison_text = comparison_highlight(sentence, corrected_text)

            # Getting our highlighted sentence by passing our input text and the grammaticaly correct sentence
            underlined_text = underline_grammar_errors(sentence, corrected_text)

            # Appending correct, comparison and highlighted sentence to their respective lists
            corrected_sentences.append("".join(corrected_text))
            comparison_sentences.append("".join(comparison_text))
            underlined_sentences.append("".join(underlined_text))

    # Combine the corrected sentences back into a paragraph
    corrected_paragraph = " ".join(corrected_sentences)
    comparison_paragraph = " ".join(comparison_sentences)
    underlined_paragraph = " ".join(underlined_sentences)

    return corrected_paragraph, comparison_paragraph, underlined_paragraph

# Function that will return paraphrased text
def paraphrase(text,num_beams=5,num_beam_groups=5,repetition_penalty=10.0,
               diversity_penalty=3.0,no_repeat_ngram_size=2,temperature=0.7,max_length=128):

    sentences = nltk.sent_tokenize(text)
    paraphrased_sentences = []

    for sentence in sentences:
        if len(sentence) <= 2:
            # print(sentence)
            pass
        else:
            input_ids = paraphrasing_tokenizer(f'paraphrase: {sentence}',return_tensors="pt", padding="longest",max_length=max_length,truncation=True).input_ids

            outputs = paraphraser_model.generate(
                input_ids, temperature=temperature, repetition_penalty=repetition_penalty,
                 no_repeat_ngram_size=no_repeat_ngram_size,
                num_beams=num_beams, num_beam_groups=num_beam_groups,
                max_length=max_length, diversity_penalty=diversity_penalty
            )
            paraphrased_text = paraphrasing_tokenizer.batch_decode(outputs, skip_special_tokens=True)
            paraphrased_sentences.append("".join(paraphrased_text[0]))

    # Combine the corrected sentences back into a paragraph
    paraphrased_paragraph = " ".join(paraphrased_sentences)

    return paraphrased_paragraph


@app.route('/')
def index():
    return "Congratulations! Your model has run successfully."


@app.route('/correct_text', methods=['POST'])
def correct_text():
    data = request.get_json()  # Get data posted as JSON
    text = data['text']
    corrected_text, _, _ = correcting_grammar(text)
    return jsonify({
        'original': text,
        'corrected': corrected_text
    })

if __name__=="__main__":
    app.run(debug=True)
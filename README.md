# Grammar-Synthesis Model

## Introduction
Welcome to the Grammar-Synthesis Model repository! This project focuses on the development of a Grammar Error Correction (GEC) model designed to enhance written language fluency and correctness.

## Table of Contents
1. [Model Overview](#model-overview)
2. [Training Process](#training-process)
3. [Challenges](#challenges)
4. [Use Case Examples](#use-case-examples)
5. [Performance Evaluation](#performance-evaluation)
6. [GEC Application](#gec-application)
7. [Limitations](#limitations)
8. [Requirements](#requirements)

## Model Overview

The Grammar-Correction transformers model that was created utilizes the Flan-T5-base pre-trained model and has been fine-tuned using the JFLEG dataset with the assistance of the Happy Transformer framework. Its primary objective is to correct a wide range of potential grammatical errors that sentences might contain including issues with punctuation, typos, prepositions, and more.

You can test the model on [HuggingFace](https://huggingface.co/Sajid030/t5-base-grammar-synthesis)

## Training Process

The fine-tuning process involved training the model on the JFLEG dataset with specific parameters:

- Epochs: 3
- Batch Size: 8
- Learning Rate: 0.0002

Check out the `Grammar_Synthesis_with_T5.ipynb` notebook for a detailed walkthrough of the training process.

## Challenges

While testing the Grammar-Synthesis model, the model faced challenges in specific use cases, some of them were:

1. Tense Correction Issues:
   
   In specific use cases, the model struggled with accurate tense corrections. For example, it failed to correct 'have' to 'had' when addressing a tense issue related to the term 'yesterday.'
   ```
   In [1]: I have seen that movie yesterday.
   Out [1]: I have seen that movie yesterday.
   ```
2. Subject-Verb Agreement Challenges:

   Instances where the model inaccurately revised phrases like 'Me and John' to 'We' instead of the correct 'John and I,' indicating difficulties in maintaining proper subject-verb agreement.
   ```
   In [2]: Me and John are going to the store
   Out [2]: We are going to the store.
   ```
   If we look at the output sentence, we can see that it is not grammatically incorrect but the model somewhat altered the initial meaning of sentence.

Identifying and addressing some of these challenges was crucial for refining the Grammar-Synthesis model and improving its overall accuracy in correcting grammatical errors.


## Use Case Examples

We present various examples showcasing the model's performance on common grammatical issues, including subject-verb agreement, run-on sentences, and more. These examples provide insights into the model's strengths and areas for improvement.

| Input                                               | Output                                             |
| ---------------------------------------------------- | -------------------------------------------------- |
| She has been crying yesterday.                       | She had been crying yesterday.                      |
| Your welcome.                                        | You are welcome.                                   |
| You're laptop is broken.                             | Your laptop is broken.                             |
| Why does you persist in blaming yourself for what happened | Why do you persist in blaming yourself for what happened? |
| With excitement, the concert tickets were purchased. | We purchased the concert tickets with excitement.  |
| I wonder about the current whether conditions.       | I wonder about the current atmospheric conditions. |
| Your welcome to join us for dinner tonight.          | You're welcome to join us for dinner tonight.      |
| I can has cheezburger.                               | I can have a cheeseburger.                         |
| Although it was raining.                             | Although it was raining, I was able to stay warm.  |
| She sings goodly.                                    | She sings well.                                    |
| She dance more better than him.                      | She dances better than him.                        |
| The new law will have a positive affect.             | The new law will have a positive effect.           |
| Its a long way to the beach.                         | It's a long way to the beach.                       |
| Their playing basketball.                            | They are playing basketball.                       |
| I won't tell you nothing about it.                   | I won't tell you anything about it.                |
| One person if don't have good health that means so many things they could lost. | If one person doesn't have good health, that means they could lose so many things. |
| Me and my sister went to the amusement park.        | My sister and I went to the amusement park.        |

## Performance Evaluation

To assess the model's effectiveness, we conducted thorough evaluations on the JFLEG test dataset using BLEU and GLEU scores. Comparative analyses with other GEC models available on Hugging Face offer a comprehensive view of our model's performance.

| Models                                       | BLEU Score | GLEU Score |
| -------------------------------------------- | ---------- | ---------- |
| OUR MODEL                                    | 82.11      | 76.66      |
| pszemraj/flan-t5-largegrammar-synthesis      | 73.13      | 69.62      |
| pszemraj/grammarsynthesis-large              | 73.08      | 68.40      |
| pszemraj/grammarsynthesis-base               | 65.24      | 62.08      |
| pszemraj/bart-basegrammar-synthesis          | 58.01      | 56.83      |
| grammarly/coedit-large                       | 82.64      | 77.49      |
| KES/T5-KES                                   | 85.31      | 80.27      |
| vagmi/grammar                                | 74.86      | 68.02      |

## GEC Application

We then developed a fully-fledged GEC application that utilizes our Grammar-Synthesis model. Key features include:

- Grammar Correction Function
- Spellchecking for Improved Output
- Two Highlighting Techniques

Use-Case example:-
```
In[3]: The sky was cloudless and the sun shines brightly on this hot summer day. I was laying by the beach, soaking up the warm rays of the sun. There were many peoples around, enjoying the ocean and playing beach volleyball. I was relax and listen to the sound of the waves crashing on the shore. Suddenly, a group of childrens started building sandcastles nearby, their laughters filling the air. As the day goes on, the temperature raises even higher, and I can feel myself getting sweatier. I decide to take a swim in the cool water to refresh. Afterward, I layed back on my towel, feeling the sand sticks to my body. As the sun sets over the horizon, the sky turns into beautiful shades of oranges and reds. It was a perfect end to a amazing day at the beach.
Out[3]: The sky was cloudless and the sun sh[i]one[s] brightly on this hot summer day. I was laying by the beach, soaking up the warm rays of the sun. There were many people[s] around, enjoying the ocean and playing beach volleyball. I was relax[]ing and listen[]ing to the sound of the waves crashing on the shore. Suddenly, a group of children[s] started building sandcastle[s] nearby, their laughters filling the air. As the day goes on, the temperature r[a]ises even higher, and I can feel myself getting sweatier. I decide to take a swim in the cool water to refresh. Afterward, I lay[ed] back on my towel, feeling the sand sticks to my body. As the sun []rise[t]s over the horizon, the sky turns into beautiful shades of oranges and reds. It was a perfect end to a[]n amazing day at the beach.
```
Explore the `Grammar_Synthesis_Application.ipynb` notebook for testing the GEC application with a text paragraph.


## Flask API
Run flask application
```
python3 grammar_synthesis_flask_api.py
```
Test flask application
```
curl -X POST http://localhost:5000/correct_text -H "Content-Type: application/json" -d "{\"text\":\"This is the text to be corrected.\"}"
```

## Limitations

While proficient in sentence-level corrections, our model still has limitations in handling entire paragraphs or documents. Contextual dependencies, especially in changing tenses, may impact overall consistency within a paragraph.

## Requirements
Ensure you have the required Python libraries by running:
```
pip install pandas happytransformer datasets scikit-learn requests nltk transformers pyspellchecker

```
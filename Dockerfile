# Use the official Python image as a base image
FROM python:3.6-slim

# Set the working directory in the container
WORKDIR /main

# Copy the Flask application code into the container
COPY . /main

# Install Flask and other dependencies
RUN pip install --no-cache-dir -r requirements.txt


# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.

 #used during cloud run
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app   
# CMD exec gunicorn --bind :8080 --workers 1 --threads 8 --timeout 0 main:app     used during local run


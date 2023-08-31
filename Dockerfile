# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Database Configuration (if needed)
# ENV DATABASE_URL sqlite:///naruto.db

# NarutoCharacter class definition (if needed)
# RUN python -c 'from your_app import db, NarutoCharacter; db.create_all()'

# Define environment variable
ENV FLASK_APP NarutoCharacter.py

# Run the Flask application when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]

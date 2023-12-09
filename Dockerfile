# Use the official Python image from Docker Hub as the base image
FROM python:3.11

# Set the working directory inside the Docker container
WORKDIR /app

# Copy the requirements file into the Docker container and install dependencies
COPY game/requirements.txt .
RUN pip install -r requirements.txt

# Copy the entire project into the Docker container
COPY . .

# Define the command to run your game
CMD ["python", "game/main.py"]
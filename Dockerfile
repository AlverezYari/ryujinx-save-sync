# Use an official Python runtime as the base image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the application code into the container
COPY . .

# Install any necessary dependencies
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside the container
EXPOSE 80

# Run the command to start the application
CMD ["python", "app.py"]
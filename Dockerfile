# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY version.py /app

# Run version.py when the container launches
CMD ["python", "version.py"]
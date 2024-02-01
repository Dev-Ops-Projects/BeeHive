# Use an official Python runtime as a parent image
FROM python@sha256:a09f71f4af992ddf9a620330fed343c850c371251be45c3f9bb46ebeca49c9c6

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install project dependencies
RUN pip install -r requirements.txt

# Expose the port your Flask application will run on (e.g., 5000)
EXPOSE 5000

# Define the command to run your Flask application
CMD ["python", "app.py"]

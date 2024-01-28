# Use an official Python runtime as a parent image
FROM python@sha256:a09f71f4af992ddf9a620330fed343c850c371251be45c3f9bb46ebeca49c9c6

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY version.py /app

# Run version.py when the container launches
CMD ["python", "version.py"]
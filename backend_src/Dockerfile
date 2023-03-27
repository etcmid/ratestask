# Base image
FROM python:3.9-alpine

# Set the working directory
WORKDIR /backend

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the application code to the working directory
COPY . .

# Set environment variables
ENV FLASK_APP=api/app.py
ENV FLASK_ENV=production

# Expose the port on which the app will run
EXPOSE 5000

# Start the application
CMD ["flask", "run", "--host=0.0.0.0"]

# Use the official Python image as the base image
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Install any system dependencies (if needed)
# For PostgreSQL, we need libpq-dev
RUN apt-get update && apt-get install -y libpq-dev

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Expose the port that your FastAPI application will run on (e.g., port 8000)
EXPOSE 8000

# Command to run your FastAPI application using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

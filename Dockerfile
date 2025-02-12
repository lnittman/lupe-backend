# Use Python 3.8 as base image
FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p uploads temp pretrained_models

# Expose port
EXPOSE 8000

# Run the application with shell to evaluate environment variables
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} 
# Use Python 3.9 as base image (supported by latest Spleeter)
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir "spleeter @ git+https://github.com/deezer/spleeter.git"

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p uploads temp pretrained_models

# Expose port
EXPOSE 8000

# Run the application using our start script
CMD ["python", "start.py"] 
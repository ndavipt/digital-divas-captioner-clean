# Use Python as base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Ensure model directory exists
RUN mkdir -p deepdanbooru_model

# Download model files if not already present
RUN if [ ! -f deepdanbooru_model/model-resnet_custom_v3.h5 ]; then \
    curl -L -o deepdanbooru_model/model-resnet_custom_v3.h5 https://github.com/KichangKim/DeepDanbooru/releases/download/v3-20211112-sgd-e28/model-resnet_custom_v3.h5; \
    fi
RUN if [ ! -f deepdanbooru_model/tags.txt ]; then \
    curl -L -o deepdanbooru_model/tags.txt https://github.com/KichangKim/DeepDanbooru/releases/download/v3-20211112-sgd-e28/tags.txt; \
    fi

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PORT=10000

# Expose the port that Render will use
EXPOSE 10000

# Command to run the application with increased timeout
# Note: Using $PORT which is provided by Render
CMD gunicorn --bind 0.0.0.0:$PORT --timeout 120 --workers 1 app:app
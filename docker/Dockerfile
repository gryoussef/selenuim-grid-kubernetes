FROM python:3.12-slim

# Install system dependencies for wget and curl (needed for healthchecks)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ .

# Create directories for results
RUN mkdir -p /app/reports /app/screenshots

# Environment variables for Grid connection
ENV SELENIUM_GRID_URL="http://selenium-hub:4444/wd/hub"
ENV PYTHONPATH=/app

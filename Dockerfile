# Use a lightweight Python base image
FROM python:3.11-slim

# Environment optimizations
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Container working directory
WORKDIR /app

# Install system dependencies for psycopg2 (safe practice even with -binary)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project source code
COPY . .

# Default command to start the experiment
CMD ["python", "main.py"]

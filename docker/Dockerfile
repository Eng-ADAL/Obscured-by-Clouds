# Use official Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements and install them
COPY requirements.txt .

# Install Linux deps + less + psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    less \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Default command: start interactive shell
CMD ["bash"]

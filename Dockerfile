# Use official Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install Linux deps + less + psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    less \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . /app

# Install Python requirements
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir psycopg[binary]

# Default command: start interactive shell
CMD ["bash"]


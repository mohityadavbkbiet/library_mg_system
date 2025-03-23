# ✅ Multi-stage build: Builder stage for dependencies
FROM python:3.11-slim AS builder

# Environment variables for efficiency
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    libmariadb-dev \
    gcc \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --prefix=/install -r requirements.txt



# ✅ Final image with only necessary files
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy necessary application files
COPY --from=builder /install /usr/local
COPY . .

# Health check to ensure the container is running properly
HEALTHCHECK --interval=30s --timeout=10s --retries=5 \
    CMD curl -f http://localhost:8000/ || exit 1

# Add wait-for-it script to ensure MySQL is ready
COPY ./wait-for-it.sh /usr/local/bin/wait-for-it.sh
RUN chmod +x /usr/local/bin/wait-for-it.sh

# Command to run migrations and start the server
CMD ["bash", "-c", "wait-for-it.sh db:3306 -- python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]

# Use official Python image
FROM python:3.10-slim-bullseye

# Set work directory
WORKDIR /app

# Install system dependencies for MySQL
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python summer/manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run Django server
CMD ["gunicorn", "summer.wsgi:application", "--bind", "0.0.0.0:8000"]

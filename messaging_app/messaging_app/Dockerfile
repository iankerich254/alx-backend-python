# Use Python 3.10 base image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libsystemd-dev \
    pkg-config \
    libcairo2-dev \
    libgirepository1.0-dev \
    python3-gi \
    gir1.2-gtk-3.0 \
    gobject-introspection \
    libffi-dev \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY messaging_app/ ./messaging_app
COPY chats/ ./chats
COPY manage.py .

# Copy project files
COPY . .

# Expose port Django runs on
EXPOSE 8000

# Default run command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# To run this container: docker run -p 8000:8000 messaging_app

# Use Python 3.10 base image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
COPY safe_install.py .
RUN python safe_install.py

# Copy project files
COPY . .

# Expose port Django runs on
EXPOSE 8000

# Default run command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


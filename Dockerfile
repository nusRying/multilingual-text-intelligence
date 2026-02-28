# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose ports for FastAPI (8000) and Streamlit (8501)
EXPOSE 8000
EXPOSE 8501

# Create a startup script to run both services (simple version)
RUN printf "#!/bin/bash\nuvicorn main:app --host 0.0.0.0 --port 8000 & \nstreamlit run dashboard.py --server.port 8501 --server.address 0.0.0.0\n" > /app/start.sh
RUN chmod +x /app/start.sh

# Default command
CMD ["/app/start.sh"]

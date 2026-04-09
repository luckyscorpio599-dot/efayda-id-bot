FROM python:3.11-slim

# Install system dependencies (including Poppler)
RUN apt-get update && apt-get install -y \
    poppler-utils \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code
COPY . .

# Start the bot
CMD ["python", "main.py"]

FROM python:3.11-slim

# Set environment variables
ENV PIP_NO_CACHE_DIR=1

# Install dependencies
RUN apt update && apt install -y \
    curl \
    git \
    gcc \
    aria2 \
    ffmpeg \
 && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /bot

# Copy all project files
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Make aria2c RPC script executable
RUN chmod +x aria.sh

# Start bot and aria2
CMD ["bash", "-c", "./aria.sh & python3 bot.py"]

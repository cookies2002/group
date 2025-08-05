# Base image
FROM python:3.11-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    aria2 \
    unzip \
    && apt-get clean

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Make aria2 script executable
RUN chmod +x aria.sh

# Expose aria2 RPC port (optional)
EXPOSE 6800

# Start bot and aria2
CMD ["bash", "-c", "./aria.sh && python3 bot.py"]

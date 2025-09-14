# Render Dockerfile for Instagram Bot
FROM python:3.11-slim

# Install Chrome and dependencies for Render
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    xvfb \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot code
COPY web_automation_bot.py .

# Create directory for Chrome profile persistence
RUN mkdir -p /app/chrome_profile

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:99

# Run the bot
CMD ["python", "web_automation_bot.py"]

# Render Dockerfile for Instagram Bot
FROM python:3.11-slim

    # Install Chrome and dependencies for Render (Fixed ChromeDriver resolution)
    RUN apt-get update && apt-get install -y \
        wget \
        gnupg \
        unzip \
        curl \
        xvfb \
        ca-certificates \
        jq \
        && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/googlechrome-keyring.gpg \
        && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/googlechrome-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
        && apt-get update \
        && apt-get install -y google-chrome-stable \
        && CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+') \
        && echo "Chrome version: $CHROME_VERSION" \
        && MAJOR_VERSION=$(echo $CHROME_VERSION | cut -d. -f1) \
        && echo "Chrome major version: $MAJOR_VERSION" \
        && LATEST_RELEASE=$(curl -s "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json" | jq -r '.channels.Stable.version') \
        && echo "Latest stable ChromeDriver version: $LATEST_RELEASE" \
        && CHROMEDRIVER_URL="https://storage.googleapis.com/chrome-for-testing-public/${LATEST_RELEASE}/linux64/chromedriver-linux64.zip" \
        && echo "Downloading ChromeDriver from: $CHROMEDRIVER_URL" \
        && wget -O /tmp/chromedriver.zip "$CHROMEDRIVER_URL" \
        && unzip /tmp/chromedriver.zip -d /tmp/ \
        && mv /tmp/chromedriver-linux64/chromedriver /usr/bin/chromedriver \
        && chmod +x /usr/bin/chromedriver \
        && chromedriver --version \
        && rm -rf /var/lib/apt/lists/* /tmp/chromedriver.zip /tmp/chromedriver-linux64# Set up working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create directory for Chrome profile persistence
RUN mkdir -p /app/chrome_profile

# Set environment variables for Render
ENV RENDER_DEPLOYMENT=true
ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:99
ENV PORT=10000

# Expose port for Render
EXPOSE 10000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:10000/status || exit 1

# Run the web service (not the bot directly)
CMD ["python", "web_service_bot.py"]
CMD ["python", "web_service_bot.py"]

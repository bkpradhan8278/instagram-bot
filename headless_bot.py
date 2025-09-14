#!/usr/bin/env python3
"""
Instagram Bot - HEADLESS MODE (No Display/Backend Operation)
Perfect for servers, VPS, or background operation without GUI
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import logging
from datetime import datetime

# Setup logging for headless operation
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("headless_bot.log"),
        logging.StreamHandler()
    ]
)

class HeadlessInstagramBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = None
        self.wait = None
        self.setup_headless_driver()
        
    def setup_headless_driver(self):
        """Setup Chrome driver for headless (no display) operation"""
        chrome_options = Options()
        
        # Headless mode settings - optimized for backend/server operation
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-software-rasterizer")
        chrome_options.add_argument("--disable-background-timer-throttling")
        chrome_options.add_argument("--disable-backgrounding-occluded-windows")
        chrome_options.add_argument("--disable-renderer-backgrounding")
        chrome_options.add_argument("--disable-features=TranslateUI")
        chrome_options.add_argument("--disable-ipc-flooding-protection")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-images")  # Faster loading
        chrome_options.add_argument("--disable-javascript")  # Only when needed
        chrome_options.add_argument("--disable-plugins-discovery")
        
        # Anti-detection settings
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        logging.info("🔇 HEADLESS MODE ACTIVATED - Running without display")
        logging.info("📱 Perfect for servers, VPS, or background operation")
        
        # Auto-install and setup ChromeDriver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.wait = WebDriverWait(self.driver, 10)
        
        logging.info("✅ Headless browser initialized successfully")

def main_headless():
    """Main function for headless operation"""
    # Configuration
    USERNAME = "bi.pali8278@gmail.com"
    PASSWORD = "Bk8278@@"
    TARGET_ACCOUNTS = [
        "udayanonmoney",
        "lavanya.das_",
        "shreeyasatapathy", 
        "bashu_sanchita"
    ]
    MAX_FOLLOWS_PER_CYCLE = 2
    
    bot = None
    try:
        logging.info("🚀 === STARTING HEADLESS INSTAGRAM BOT ===")
        logging.info("🔇 No display mode - Perfect for backend operation")
        
        # Import the main bot functionality but force headless mode
        import web_automation_bot
        
        # Create bot instance in headless mode
        bot = web_automation_bot.InstagramWebBot(USERNAME, PASSWORD, headless=True)
        
        # Login
        if bot.login():
            logging.info("✅ Login successful in headless mode")
            # Run continuous 24/7 campaign
            bot.run_continuous_campaign(TARGET_ACCOUNTS, MAX_FOLLOWS_PER_CYCLE)
        else:
            logging.error("❌ Login failed in headless mode")
            
    except KeyboardInterrupt:
        logging.info("⏹️ Bot stopped by user (Ctrl+C)")
    except Exception as e:
        logging.exception(f"💥 Headless bot error: {e}")
    finally:
        if bot:
            bot.close()
            logging.info("🔇 Headless browser closed")

if __name__ == "__main__":
    main_headless()

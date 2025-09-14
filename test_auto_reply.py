#!/usr/bin/env python3
"""
Test script to debug auto-reply functionality
"""

import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler('test_auto_reply.log'),
        logging.StreamHandler()
    ]
)

class AutoReplyTester:
    def __init__(self):
        self.driver = None
        
    def setup_browser(self):
        """Setup Chrome browser with stealth settings"""
        try:
            chrome_options = Options()
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--allow-running-insecure-content")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Execute script to hide automation detection
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            logging.info("Browser setup complete")
            return True
            
        except Exception as e:
            logging.error(f"Failed to setup browser: {e}")
            return False
    
    def human_delay(self, min_seconds=2, max_seconds=4):
        """Add human-like delay"""
        import random
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
    
    def login_instagram(self):
        """Login to Instagram"""
        try:
            logging.info("Navigating to Instagram...")
            self.driver.get("https://www.instagram.com/accounts/login/")
            self.human_delay(3, 5)
            
            # Enter username
            username_input = self.driver.find_element(By.NAME, "username")
            username_input.send_keys("bi.pali8278@gmail.com")
            self.human_delay(1, 2)
            
            # Enter password
            password_input = self.driver.find_element(By.NAME, "password")
            password_input.send_keys("Bk8278@@")
            self.human_delay(1, 2)
            
            # Click login
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            logging.info("Login submitted, waiting for response...")
            self.human_delay(5, 8)
            
            # Check if login was successful
            if "instagram.com" in self.driver.current_url and "login" not in self.driver.current_url:
                logging.info("Login successful!")
                return True
            else:
                logging.error("Login failed or requires additional verification")
                return False
                
        except Exception as e:
            logging.error(f"Login error: {e}")
            return False
    
    def test_message_detection(self):
        """Test the message detection and auto-reply system"""
        try:
            logging.info("Testing message detection...")
            
            # Go to messages/DMs
            logging.info("Navigating to messages...")
            self.driver.get("https://www.instagram.com/direct/inbox/")
            self.human_delay(4, 6)
            
            # Log current page source to debug
            page_title = self.driver.title
            current_url = self.driver.current_url
            logging.info(f"Current page title: {page_title}")
            logging.info(f"Current URL: {current_url}")
            
            # Try multiple selectors for message threads
            selectors_to_try = [
                "//div[contains(@class, 'unread')]//div[contains(@role, 'button')]",
                "//div[@role='button']//div[contains(@dir, 'auto')]",
                "//div[@role='button'][contains(., '@')]",
                "//a[contains(@href, '/direct/t/')]",
                "//div[contains(@class, 'x1i10hfl')]",  # Common Instagram class
                "//div[text()][parent::div[@role='button']]"
            ]
            
            found_threads = []
            
            for i, selector in enumerate(selectors_to_try):
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    logging.info(f"Selector {i+1}: Found {len(elements)} elements with '{selector}'")
                    
                    if elements:
                        for j, element in enumerate(elements[:3]):  # Check first 3
                            try:
                                text = element.text.strip()
                                if text:
                                    logging.info(f"  Element {j+1} text: '{text[:50]}...'")
                                    found_threads.append((element, text))
                            except:
                                logging.info(f"  Element {j+1}: Could not get text")
                                
                except Exception as e:
                    logging.warning(f"Selector {i+1} failed: {e}")
            
            if found_threads:
                logging.info(f"Found {len(found_threads)} potential message threads")
                
                # Try to click on the first thread
                try:
                    logging.info("Attempting to click first message thread...")
                    found_threads[0][0].click()
                    self.human_delay(3, 5)
                    
                    # Check if we're in a conversation
                    current_url_after = self.driver.current_url
                    logging.info(f"URL after clicking thread: {current_url_after}")
                    
                    # Try to find message elements
                    message_selectors = [
                        "//div[@role='main']//div[contains(@style, 'text-align')]",
                        "//div[contains(@class, 'message')]",
                        "//span[contains(@dir, 'auto')]",
                        "//div[contains(@data-testid, 'message')]"
                    ]
                    
                    for selector in message_selectors:
                        try:
                            messages = self.driver.find_elements(By.XPATH, selector)
                            logging.info(f"Found {len(messages)} messages with selector: {selector}")
                            
                            if messages:
                                for i, msg in enumerate(messages[-3:]):  # Last 3 messages
                                    try:
                                        msg_text = msg.text.strip()
                                        if msg_text:
                                            logging.info(f"  Message {i+1}: '{msg_text}'")
                                    except:
                                        pass
                                break
                        except Exception as e:
                            logging.warning(f"Message selector failed: {e}")
                    
                    # Try to find message input box
                    input_selectors = [
                        "//textarea[@placeholder='Message...' or @aria-label='Message']",
                        "//textarea[contains(@placeholder, 'message')]",
                        "//div[@contenteditable='true']",
                        "//input[@placeholder='Message...']"
                    ]
                    
                    for selector in input_selectors:
                        try:
                            input_box = self.driver.find_element(By.XPATH, selector)
                            logging.info(f"SUCCESS: Found message input box with selector: {selector}")
                            break
                        except:
                            logging.info(f"No input box found with selector: {selector}")
                    
                except Exception as e:
                    logging.error(f"Error clicking message thread: {e}")
                    
            else:
                logging.warning("No message threads found to test")
                
            # Take a screenshot for debugging
            try:
                self.driver.save_screenshot('test_auto_reply_debug.png')
                logging.info("Screenshot saved as test_auto_reply_debug.png")
            except Exception as e:
                logging.warning(f"Could not save screenshot: {e}")
                
        except Exception as e:
            logging.error(f"Error in message detection test: {e}")
    
    def cleanup(self):
        """Clean up resources"""
        if self.driver:
            self.driver.quit()
            logging.info("Browser closed")

def main():
    tester = AutoReplyTester()
    
    try:
        if not tester.setup_browser():
            return
            
        if not tester.login_instagram():
            return
            
        tester.test_message_detection()
        
        # Keep browser open for manual inspection
        input("Press Enter to close browser and exit...")
        
    except KeyboardInterrupt:
        logging.info("Test interrupted by user")
    except Exception as e:
        logging.error(f"Test failed: {e}")
    finally:
        tester.cleanup()

if __name__ == "__main__":
    main()

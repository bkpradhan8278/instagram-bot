"""
Instagram Web Automation Bot - Conservative Version
==================================================

CURRENT FEATURES:
- 24/7 continuous automation with intelligent cycling
- Reciprocal engagement (returns likes/comments to users who engage with your posts)
- Follow campaigns on target accounts with engagement
- Home page post engagement 
- Enhanced anti-detection with stealth browser settings
- Headless mode support for background operation
- Advanced error handling and recovery systems
- Safe operation wrappers to prevent crashes

FAST SETTINGS (15 followers in 15 minutes):
- MAX_FOLLOWS_PER_CYCLE: 15 (for quick sessions)
- Delays between users: 45-75 seconds (1 follower per minute)
- Cycle breaks: Minimal for 15-minute sessions
- Expected session follows: 15 in 15 minutes (OPTIMIZED)

REMOVED FEATURES:
- Auto-reply functionality (removed as requested)
- Direct message automation

TARGET ACCOUNTS: lavanya.das_, shreeyasatapathy, bashu_sanchita
CREDENTIALS: Set via environment variables (INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)

Run with: python web_automation_bot.py
Setup: Set environment variables before running
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import logging
import os
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("web_automation.log"),
        logging.StreamHandler()
    ]
)

class InstagramWebBot:
    def __init__(self, username, password, headless=False):
        self.username = username
        self.password = password
        self.driver = None
        self.wait = None
        self.setup_driver(headless)
        
    def setup_driver(self, headless=False):
        """Setup Chrome driver with human-like settings and session persistence"""
        chrome_options = Options()
        
        # SESSION PERSISTENCE - Use a persistent user data directory
        import os
        user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
        chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
        chrome_options.add_argument("--profile-directory=Instagram_Bot")
        
        # Human-like browser settings
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Enhanced headless mode settings
        if headless:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1366,768")  # Reduced from 1920x1080
            chrome_options.add_argument("--disable-software-rasterizer")
            chrome_options.add_argument("--disable-background-timer-throttling")
            chrome_options.add_argument("--disable-backgrounding-occluded-windows")
            chrome_options.add_argument("--disable-renderer-backgrounding")
            chrome_options.add_argument("--disable-features=TranslateUI")
            chrome_options.add_argument("--disable-ipc-flooding-protection")
            
            # Render-specific optimizations for memory constraints
            chrome_options.add_argument("--memory-pressure-off")
            chrome_options.add_argument("--max_old_space_size=512")  # Reduced from 4096
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-setuid-sandbox")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-plugins")
            chrome_options.add_argument("--disable-images")  # Disable image loading to save memory
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--disable-features=VizDisplayCompositor")
            chrome_options.add_argument("--disable-background-networking")
            chrome_options.add_argument("--disable-default-apps")
            chrome_options.add_argument("--disable-hang-monitor")
            chrome_options.add_argument("--disable-popup-blocking")
            chrome_options.add_argument("--disable-prompt-on-repost")
            chrome_options.add_argument("--disable-sync")
            chrome_options.add_argument("--disable-translate")
            chrome_options.add_argument("--disable-web-resources")
            chrome_options.add_argument("--single-process")  # Use single process to reduce memory
            chrome_options.add_argument("--no-first-run")
            chrome_options.add_argument("--no-default-browser-check")
            chrome_options.add_argument("--disable-default-apps")
            chrome_options.add_argument("--disable-component-update")
            
            # Additional memory optimization
            chrome_options.add_argument("--aggressive-cache-discard")
            chrome_options.add_argument("--memory-pressure-off")
            
            logging.info("🔇 HEADLESS MODE: Running without display (perfect for servers/background)")
        else:
            logging.info("🖥️ VISUAL MODE: Running with browser display")
            
        # Auto-install and setup ChromeDriver with Docker compatibility
        try:
            # Try to use system chromedriver first (for Docker)
            service = Service("/usr/bin/chromedriver")
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            logging.info("✅ Using system chromedriver")
        except Exception as e:
            logging.info(f"System chromedriver not found: {e}")
            try:
                # Fallback to webdriver-manager with explicit path fixing
                driver_path = ChromeDriverManager().install()
                # Fix the path if it points to wrong file
                if "THIRD_PARTY_NOTICES" in driver_path:
                    import os
                    driver_dir = os.path.dirname(driver_path)
                    actual_driver = os.path.join(driver_dir, "chromedriver")
                    if os.path.exists(actual_driver):
                        driver_path = actual_driver
                    else:
                        # Look for chromedriver in subdirectories
                        for root, dirs, files in os.walk(driver_dir):
                            for file in files:
                                if file == "chromedriver":
                                    driver_path = os.path.join(root, file)
                                    break
                            if driver_path.endswith("chromedriver"):
                                break
                
                service = Service(driver_path)
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                logging.info(f"✅ Using webdriver-manager: {driver_path}")
            except Exception as e2:
                logging.error(f"❌ ChromeDriver setup failed: {e2}")
                raise
        
        # Enhanced anti-detection for headless mode with error handling
        try:
            self.driver.execute_script("""
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
                Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
                window.chrome = {runtime: {}};
            """)
        except Exception as e:
            logging.warning(f"Could not execute anti-detection script: {e}")
        
        self.wait = WebDriverWait(self.driver, 20)  # Increased timeout for headless
        
    def is_logged_in(self):
        """Check if already logged in to avoid repeated login challenges"""
        try:
            # Go to Instagram and check for login indicators
            self.driver.get("https://www.instagram.com/")
            self.human_delay(3, 5)
            
            # Look for elements that indicate we're logged in
            logged_in_indicators = [
                "//a[@aria-label='Home']",
                "//svg[@aria-label='Home']",
                "//a[contains(@href, '/direct/')]",  # Direct messages
                "//svg[@aria-label='New post']",
                "//button[contains(@aria-label, 'New post')]"
            ]
            
            for indicator in logged_in_indicators:
                if self.driver.find_elements(By.XPATH, indicator):
                    logging.info("✅ Already logged in - skipping login process")
                    return True
            
            # Check if we're on login page
            if "accounts/login" in self.driver.current_url:
                logging.info("🔑 Not logged in - login required")
                return False
            
            # Additional check for profile elements
            try:
                profile_elements = self.driver.find_elements(By.CSS_SELECTOR, "img[alt*='profile picture']")
                if profile_elements:
                    logging.info("✅ Profile elements found - already logged in")
                    return True
            except:
                pass
                
            return False
            
        except Exception as e:
            logging.warning(f"Could not verify login status: {e}")
            return False
        
    def human_delay(self, min_sec=1, max_sec=3):
        """Random delay to mimic human behavior"""
        delay = random.uniform(min_sec, max_sec)
        time.sleep(delay)
        
    def human_type(self, element, text):
        """Type text with human-like delays"""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.2))
            
    def scroll_slowly(self, pixels=300):
        """Scroll slowly like a human"""
        current_scroll = 0
        while current_scroll < pixels:
            scroll_step = random.randint(50, 100)
            self.driver.execute_script(f"window.scrollBy(0, {scroll_step})")
            current_scroll += scroll_step
            time.sleep(random.uniform(0.1, 0.3))
            
    def login(self):
        """Login to Instagram through web interface with enhanced headless compatibility"""
        try:
            # Check if already logged in first
            if self.is_logged_in():
                return True
                
            logging.info("Opening Instagram login page...")
            self.driver.get("https://www.instagram.com/accounts/login/")
            self.human_delay(5, 8)  # Extended delay for headless mode
            
            # Handle cookie banner if present - FIXED SELECTORS
            try:
                # Try multiple cookie selector strategies
                cookie_accepted = False
                
                # Method 1: XPath selectors
                xpath_selectors = [
                    "//button[contains(text(), 'Accept')]",
                    "//button[contains(text(), 'Allow')]", 
                    "//button[contains(text(), 'Accept All')]",
                    "//button[contains(text(), 'OK')]",
                    "//button[contains(text(), 'I Accept')]"
                ]
                
                for selector in xpath_selectors:
                    try:
                        cookie_button = self.driver.find_element(By.XPATH, selector)
                        cookie_button.click()
                        logging.info(f"✅ Accepted cookies via XPath: {selector}")
                        cookie_accepted = True
                        self.human_delay(1, 2)
                        break
                    except:
                        continue
                
                # Method 2: CSS selectors if XPath failed
                if not cookie_accepted:
                    css_selectors = [
                        "button[data-cookiebanner='accept_button']",
                        "button[aria-label*='Accept']",
                        "button[aria-label*='accept']",
                        ".cookie-banner button",
                        "[role='button'][tabindex='0']"
                    ]
                    
                    for selector in css_selectors:
                        try:
                            cookie_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                            cookie_button.click()
                            logging.info(f"✅ Accepted cookies via CSS: {selector}")
                            cookie_accepted = True
                            self.human_delay(1, 2)
                            break
                        except:
                            continue
                
                # Method 3: Generic button detection (IMPROVED - exclude Facebook login)
                if not cookie_accepted:
                    try:
                        buttons = self.driver.find_elements(By.TAG_NAME, "button")
                        for button in buttons:
                            button_text = button.text.lower()
                            # Exclude Facebook login and other non-cookie buttons
                            if any(word in button_text for word in ['accept', 'allow', 'ok', 'agree']) and not any(exclude in button_text for exclude in ['facebook', 'log in', 'login', 'sign']):
                                button.click()
                                logging.info(f"✅ Accepted cookies via generic button: {button_text}")
                                cookie_accepted = True
                                self.human_delay(1, 2)
                                break
                    except:
                        pass
                        
                if not cookie_accepted:
                    logging.info("ℹ️ No cookie banner found or already accepted")
                    
            except Exception as e:
                logging.warning(f"Cookie banner handling failed: {e}")
                pass
                
            # Find username field with multiple strategies
            logging.info("Entering username...")
            username_input = None
            username_selectors = [
                (By.NAME, "username"),
                (By.CSS_SELECTOR, "input[name='username']"),
                (By.CSS_SELECTOR, "input[type='text']"),
                (By.XPATH, "//input[@placeholder='Phone number, username, or email']"),
                (By.XPATH, "//input[contains(@class, 'username')]")
            ]
            
            for selector_type, selector in username_selectors:
                try:
                    username_input = self.wait.until(EC.presence_of_element_located((selector_type, selector)))
                    break
                except:
                    continue
                    
            if not username_input:
                raise Exception("Could not find username field")
                
            username_input.click()
            self.human_delay(0.5, 1)
            username_input.clear()
            self.human_type(username_input, self.username)
            
            # Find password field with multiple strategies
            logging.info("Entering password...")
            password_input = None
            password_selectors = [
                (By.NAME, "password"),
                (By.CSS_SELECTOR, "input[name='password']"),
                (By.CSS_SELECTOR, "input[type='password']"),
                (By.XPATH, "//input[@placeholder='Password']")
            ]
            
            for selector_type, selector in password_selectors:
                try:
                    password_input = self.driver.find_element(selector_type, selector)
                    break
                except:
                    continue
                    
            if not password_input:
                raise Exception("Could not find password field")
                
            password_input.click()
            self.human_delay(0.5, 1)
            password_input.clear()
            self.human_type(password_input, self.password)
            
            # Click login button with multiple strategies
            self.human_delay(1, 2)
            login_button = None
            login_selectors = [
                (By.XPATH, "//button[@type='submit']"),
                (By.XPATH, "//button[contains(text(), 'Log in')]"),
                (By.XPATH, "//button[contains(text(), 'Log In')]"),
                (By.CSS_SELECTOR, "button[type='submit']"),
                (By.XPATH, "//div[@role='button'][contains(text(), 'Log')]")
            ]
            
            for selector_type, selector in login_selectors:
                try:
                    login_button = self.driver.find_element(selector_type, selector)
                    # Verify this is actually a login button and not something else
                    button_text = login_button.text.lower()
                    if 'log' in button_text and 'facebook' not in button_text:
                        logging.info(f"Found login button: {login_button.text}")
                        break
                    else:
                        login_button = None
                except:
                    continue
                    
            if login_button:
                try:
                    login_button.click()
                    logging.info("✅ Clicked login button")
                except Exception as e:
                    logging.warning(f"Could not click login button: {e}")
                    # Fallback: press Enter on password field
                    password_input.send_keys(Keys.RETURN)
                    logging.info("⌨️ Used Enter key as fallback")
            else:
                # Fallback: press Enter on password field
                password_input.send_keys(Keys.RETURN)
                logging.info("⌨️ No login button found, using Enter key")
            
            # Wait for login to complete with timeout
            logging.info("Waiting for login to complete...")
            self.human_delay(8, 12)  # Extended delay for headless mode
            
            # Check login status with timeout
            max_login_attempts = 3
            for login_attempt in range(max_login_attempts):
                try:
                    current_url = self.driver.current_url
                    if "instagram.com" in current_url and not "accounts/login" in current_url:
                        logging.info("✅ Login successful - redirected from login page!")
                        break
                    elif login_attempt < max_login_attempts - 1:
                        logging.info(f"Still on login page, waiting... (attempt {login_attempt + 1}/{max_login_attempts})")
                        self.human_delay(5, 8)
                    else:
                        logging.warning("Login process taking longer than expected")
                except Exception as e:
                    logging.warning(f"Error checking login status: {e}")
                    self.human_delay(3, 5)
            
            # Handle "Save Info" dialog
            try:
                not_now_selectors = [
                    "//button[contains(text(), 'Not Now')]",
                    "//button[contains(text(), 'Not now')]",
                    "//button[contains(text(), 'Save Info')]/../following-sibling::button"
                ]
                for selector in not_now_selectors:
                    try:
                        not_now_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                        not_now_button.click()
                        self.human_delay(2, 3)
                        break
                    except:
                        continue
            except:
                pass
                
            # Handle notifications dialog
            try:
                for selector in not_now_selectors:
                    try:
                        not_now_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                        not_now_button.click()
                        self.human_delay(2, 3)
                        break
                    except:
                        continue
            except:
                pass
                
            # Verify login success with multiple checks
            try:
                current_url = self.driver.current_url
                logging.info(f"Current URL after login: {current_url}")
                
                # Check URL-based success
                if "instagram.com" in current_url and not "accounts/login" in current_url:
                    logging.info("✅ LOGIN SUCCESSFUL - URL verification passed!")
                    return True
                
                # Check for login indicators even if URL hasn't changed yet
                login_success_indicators = [
                    "//a[@aria-label='Home']",
                    "//svg[@aria-label='Home']",
                    "//a[contains(@href, '/direct/')]",
                    "//button[contains(@aria-label, 'New post')]"
                ]
                
                for indicator in login_success_indicators:
                    if self.driver.find_elements(By.XPATH, indicator):
                        logging.info("✅ LOGIN SUCCESSFUL - UI elements found!")
                        return True
                
                # If still on login page, check for errors
                if "accounts/login" in current_url:
                    # Check for error messages
                    error_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'incorrect') or contains(text(), 'error') or contains(text(), 'try again')]")
                    if error_elements:
                        logging.error(f"❌ Login error detected: {error_elements[0].text}")
                        return False
                    else:
                        logging.error("❌ Login verification failed - still on login page without clear error")
                        return False
                else:
                    logging.info("✅ LOGIN SUCCESSFUL - not on login page anymore!")
                    return True
                    
            except Exception as e:
                logging.error(f"❌ Error during login verification: {e}")
                return False
            
        except Exception as e:
            logging.error(f"❌ Login failed: {e}")
            return False
            
    def close_modal(self):
        """Close any open modals or dialogs"""
        try:
            # Try different ways to close modals
            close_buttons = [
                "//button[@aria-label='Close']",
                "//button[contains(@class, 'close')]", 
                "//svg[@aria-label='Close']/..",
                "//div[@role='button' and contains(@aria-label, 'Close')]"
            ]
            
            for xpath in close_buttons:
                try:
                    close_btn = self.driver.find_element(By.XPATH, xpath)
                    close_btn.click()
                    self.human_delay(1, 2)
                    return True
                except:
                    continue
                    
            # Try pressing Escape key
            from selenium.webdriver.common.keys import Keys
            self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
            self.human_delay(1, 2)
            return True
            
        except Exception as e:
            logging.warning(f"Could not close modal: {e}")
            return False
            
    def visit_profile(self, username):
        """Visit a user's profile"""
        try:
            profile_url = f"https://www.instagram.com/{username}/"
            logging.info(f"Visiting profile: @{username}")
            self.driver.get(profile_url)
            self.human_delay(3, 5)
            return True
        except Exception as e:
            logging.error(f"Failed to visit profile @{username}: {e}")
            return False
            
    def get_followers_list(self, max_followers=15):
        """Get list of followers from current profile"""
        try:
            # Try to find followers link with multiple selectors
            followers_link = None
            
            # Method 1: Try href-based selector
            try:
                followers_link = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/followers/')]")))
            except:
                # Method 2: Try text-based selector
                try:
                    followers_link = self.driver.find_element(By.XPATH, "//a[contains(text(), 'followers') or contains(text(), 'Followers')]")
                except:
                    # Method 3: Try span containing followers count
                    try:
                        followers_elements = self.driver.find_elements(By.XPATH, "//span[contains(text(), 'followers')]/..")
                        if followers_elements:
                            followers_link = followers_elements[0]
                    except:
                        pass
            
            if not followers_link:
                logging.warning("Could not find followers link")
                return []
                
            followers_link.click()
            self.human_delay(4, 6)
            
            followers = []
            seen_usernames = set()
            
            # Look for followers in the dialog
            for scroll_count in range(3):  # Reduced scrolling
                # Try multiple selectors for follower links
                follower_elements = []
                
                # Method 1: Standard dialog links
                try:
                    follower_elements = self.driver.find_elements(By.XPATH, "//div[@role='dialog']//a[contains(@href, '/') and not(contains(@href, '/p/'))]")
                except:
                    pass
                    
                # Method 2: Any profile links in modal
                if not follower_elements:
                    try:
                        follower_elements = self.driver.find_elements(By.XPATH, "//div[contains(@style, 'overflow')]//a[contains(@href, '/')]")
                    except:
                        pass
                
                for element in follower_elements[:max_followers]:
                    try:
                        href = element.get_attribute('href')
                        if href and '/p/' not in href and href.count('/') >= 4:
                            username = href.split('/')[-2] if href.endswith('/') else href.split('/')[-1]
                            if username and username not in seen_usernames and len(followers) < max_followers:
                                followers.append(username)
                                seen_usernames.add(username)
                                logging.info(f"Found follower: @{username}")
                    except:
                        continue
                        
                if len(followers) >= max_followers:
                    break
                    
                # Scroll in the dialog
                try:
                    # Try to find scrollable area
                    scrollable_area = None
                    try:
                        scrollable_area = self.driver.find_element(By.XPATH, "//div[@role='dialog']//div[contains(@style, 'overflow') or contains(@style, 'scroll')]")
                    except:
                        try:
                            scrollable_area = self.driver.find_element(By.XPATH, "//div[@role='dialog']")
                        except:
                            pass
                    
                    if scrollable_area:
                        self.driver.execute_script("arguments[0].scrollTop += 200", scrollable_area)
                        self.human_delay(2, 3)
                except:
                    break
                
            # Close dialog with multiple methods
            self.close_modal_dialog()
            
            logging.info(f"Found {len(followers)} followers")
            return followers
            
        except Exception as e:
            logging.error(f"Failed to get followers: {e}")
            return []
            
    def close_modal_dialog(self):
        """Close any modal dialog with multiple fallback methods"""
        try:
            # Method 1: Close button with aria-label
            try:
                close_button = self.driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Close') or contains(@aria-label, 'close')]")
                close_button.click()
                self.human_delay(1, 2)
                return
            except:
                pass
                
            # Method 2: X button (SVG)
            try:
                close_button = self.driver.find_element(By.XPATH, "//svg[@aria-label='Close' or @aria-label='close']/..")
                close_button.click()
                self.human_delay(1, 2)
                return
            except:
                pass
                
            # Method 3: Any button in dialog header
            try:
                close_button = self.driver.find_element(By.XPATH, "//div[@role='dialog']//header//button")
                close_button.click()
                self.human_delay(1, 2)
                return
            except:
                pass
                
            # Method 4: Press ESC key
            try:
                from selenium.webdriver.common.keys import Keys
                self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
                self.human_delay(1, 2)
                return
            except:
                pass
                
            # Method 5: Click outside dialog (backdrop)
            try:
                backdrop = self.driver.find_element(By.XPATH, "//div[@role='presentation' or contains(@style, 'position: fixed')]")
                backdrop.click()
                self.human_delay(1, 2)
                return
            except:
                pass
                
        except Exception as e:
            logging.warning(f"Could not close modal: {e}")
            # Continue anyway
            
    def follow_user(self, username):
        """Follow a specific user with improved Instagram UI detection"""
        try:
            if not self.visit_profile(username):
                return False
                
            # Wait for page to load completely
            self.human_delay(3, 5)
                
            # Check if already following first - IMPROVED CHECK
            try:
                # Look for "Following" button or "Message" button (indicates already following)
                following_indicators = self.driver.find_elements(By.XPATH, 
                    "//button[contains(text(), 'Following') or contains(text(), 'Message') or contains(text(), 'Requested')]")
                if following_indicators:
                    logging.info(f"Already following/requested @{username} - skipping")
                    return "already_following"  # Return special status instead of True
            except:
                pass
                
            # Look for follow button with improved selectors based on current Instagram UI
            follow_button = None
            
            # Method 1: Exact "Follow" text (most reliable for current UI)
            try:
                follow_button = self.driver.find_element(By.XPATH, "//button[text()='Follow']")
                logging.info(f"Found Follow button (Method 1) for @{username}")
            except:
                # Method 2: Follow button with blue background styling
                try:
                    follow_button = self.driver.find_element(By.XPATH, 
                        "//button[text()='Follow' and contains(@style, 'background-color')]")
                    logging.info(f"Found Follow button (Method 2) for @{username}")
                except:
                    # Method 3: Follow button in profile header area
                    try:
                        follow_button = self.driver.find_element(By.XPATH, 
                            "//main//header//button[text()='Follow']")
                        logging.info(f"Found Follow button (Method 3) for @{username}")
                    except:
                        # Method 4: Any button containing Follow text (case insensitive)
                        try:
                            follow_button = self.driver.find_element(By.XPATH, 
                                "//button[contains(translate(text(), 'FOLLOW', 'follow'), 'follow') and not(contains(translate(text(), 'FOLLOWING', 'following'), 'following'))]")
                            logging.info(f"Found Follow button (Method 4) for @{username}")
                        except:
                            # Method 5: Search all buttons for Follow text
                            try:
                                buttons = self.driver.find_elements(By.TAG_NAME, "button")
                                for button in buttons:
                                    button_text = button.text.strip()
                                    if button_text == "Follow":
                                        follow_button = button
                                        logging.info(f"Found Follow button (Method 5) for @{username}")
                                        break
                            except:
                                pass
            
            if follow_button:
                try:
                    # Ensure button is visible and scroll if needed
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", follow_button)
                    self.human_delay(1, 2)
                    
                    # Try normal click first
                    try:
                        follow_button.click()
                    except:
                        # If normal click fails, try JavaScript click
                        self.driver.execute_script("arguments[0].click();", follow_button)
                    
                    # Wait a moment to see if follow was successful
                    self.human_delay(3, 4)
                    
                    # Verify follow was successful by looking for "Following" or "Requested"
                    try:
                        success_indicators = self.driver.find_elements(By.XPATH, 
                            "//button[contains(text(), 'Following') or contains(text(), 'Requested') or contains(text(), 'Message')]")
                        if success_indicators:
                            logging.info(f"SUCCESS: Successfully followed @{username}")
                            return True
                        else:
                            # Check if Follow button disappeared (another success indicator)
                            follow_check = self.driver.find_elements(By.XPATH, "//button[text()='Follow']")
                            if not follow_check:
                                logging.info(f"SUCCESS: Followed @{username} (Follow button disappeared)")
                                return True
                            else:
                                logging.warning(f"Follow button clicked but still visible for @{username}")
                                return False
                    except:
                        logging.info(f"SUCCESS: Followed @{username} (assuming success)")
                        return True
                    
                except Exception as e:
                    logging.warning(f"Could not click follow button for @{username}: {e}")
                    return False
            else:
                logging.warning(f"Could not find follow button for @{username}")
                return False
                
        except Exception as e:
            logging.error(f"Error following @{username}: {e}")
            return False
            
    def like_recent_posts(self, username, max_likes=1):
        """Like recent posts of a user - improved for current Instagram UI"""
        try:
            if not self.visit_profile(username):
                return 0
                
            self.human_delay(3, 5)
                
            # Look for posts in the profile grid with improved detection
            post_links = []
            
            # Check if user has posts
            try:
                # Look for "posts" count in profile header
                posts_text = self.driver.find_elements(By.XPATH, "//main//header//*[contains(text(), 'post')]")
                if posts_text:
                    posts_count_text = posts_text[0].text
                    if "0 post" in posts_count_text:
                        logging.info(f"@{username} has 0 posts")
                        return 0
            except:
                pass
            
            try:
                # Method 1: Look for clickable post images in grid
                post_elements = self.driver.find_elements(By.XPATH, "//article//div//a[contains(@href, '/p/')]")
                if not post_elements:
                    # Method 2: Alternative approach - look for images with parent links
                    images = self.driver.find_elements(By.XPATH, "//img[@decoding='auto']")
                    for img in images:
                        try:
                            # Find parent link
                            parent_link = img.find_element(By.XPATH, "./ancestor::a[contains(@href, '/p/')]")
                            if parent_link not in post_elements:
                                post_elements.append(parent_link)
                        except:
                            continue
                
                # Get up to max_likes posts
                for element in post_elements[:max_likes]:
                    href = element.get_attribute('href')
                    if href and '/p/' in href:
                        post_links.append(href)
                        
            except Exception as e:
                logging.warning(f"Error finding posts for @{username}: {e}")
            
            if not post_links:
                logging.warning(f"No posts found for @{username}")
                return 0
                
            likes_count = 0
            
            for post_url in post_links:
                try:
                    logging.info(f"Visiting post: {post_url}")
                    self.driver.get(post_url)
                    self.human_delay(4, 6)  # Wait for post to load
                    
                    # Check if already liked first
                    already_liked = False
                    try:
                        # Method 1: Look for Unlike button
                        unlike_buttons = self.driver.find_elements(By.XPATH, "//button//svg[@aria-label='Unlike']")
                        if unlike_buttons:
                            logging.info(f"Post already liked by @{username}")
                            already_liked = True
                            continue
                        
                        # Method 2: Look for red/filled heart
                        red_hearts = self.driver.find_elements(By.XPATH, "//svg[contains(@fill, '#ed4956') or contains(@fill, 'rgb(237, 73, 86)')]")
                        if red_hearts:
                            logging.info(f"Post already liked by @{username}")
                            already_liked = True
                            continue
                    except:
                        pass
                    
                    if not already_liked:
                        # Find and click like button - IMPROVED DETECTION
                        like_button = None
                        try:
                            # Method 1: Look for Like button with SVG
                            like_buttons = self.driver.find_elements(By.XPATH, "//button[.//svg[@aria-label='Like']]")
                            if like_buttons:
                                like_button = like_buttons[0]
                        except:
                            try:
                                # Method 2: Look for heart icon by role
                                like_button = self.driver.find_element(By.XPATH, "//span[@role='button'][.//svg[@aria-label='Like']]")
                            except:
                                try:
                                    # Method 3: Look for any button containing heart SVG
                                    heart_svgs = self.driver.find_elements(By.XPATH, "//svg[contains(.//path/@d, 'M16.792') or contains(.//path/@d, 'M20.84')]")
                                    if heart_svgs:
                                        like_button = heart_svgs[0].find_element(By.XPATH, "./ancestor::button | ./ancestor::span[@role='button']")
                                except:
                                    pass
                        
                        if like_button:
                            try:
                                # Scroll to like button and click
                                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", like_button)
                                self.human_delay(1, 2)
                                
                                # Try clicking the like button
                                try:
                                    like_button.click()
                                except:
                                    # If normal click fails, try JavaScript click
                                    self.driver.execute_script("arguments[0].click();", like_button)
                                
                                # Verify like was successful
                                self.human_delay(2, 3)
                                try:
                                    # Check for Unlike button or red heart
                                    success_indicators = self.driver.find_elements(By.XPATH, 
                                        "//button//svg[@aria-label='Unlike'] | //svg[contains(@fill, '#ed4956')]")
                                    if success_indicators:
                                        likes_count += 1
                                        logging.info(f"SUCCESS: Liked post by @{username}")
                                        
                                        # Add comment after liking
                                        self.add_comment_to_post(username)
                                        
                                    else:
                                        likes_count += 1
                                        logging.info(f"SUCCESS: Liked post by @{username} (assuming success)")
                                        
                                        # Add comment after liking  
                                        self.add_comment_to_post(username)
                                except:
                                    likes_count += 1
                                    logging.info(f"SUCCESS: Liked post by @{username}")
                                    
                                    # Add comment after liking
                                    self.add_comment_to_post(username)
                                
                                self.human_delay(5, 8)  # Wait before next action
                                
                            except Exception as e:
                                logging.warning(f"Could not click like button for @{username}: {e}")
                        else:
                            logging.warning(f"Could not find like button for @{username}")
                        
                except Exception as e:
                    logging.warning(f"Could not process post for @{username}: {e}")
                    continue
                    
            return likes_count
            
        except Exception as e:
            logging.error(f"Error liking posts by @{username}: {e}")
            return 0
            
    def add_comment_to_post(self, username):
        """Add a random comment to the current post"""
        try:
            # Random comments list
            comments = [
                "Nice!", "Amazing!", "Great post!", "Love it!", "Beautiful!", 
                "Awesome!", "Cool!", "Perfect!", "Wow!", "Fantastic!",
                "❤️", "🔥", "💯", "👍", "😍", "🙌", "✨"
            ]
            
            # 70% chance to add comment (to avoid spam detection)
            if random.random() < 0.7:
                comment_text = random.choice(comments)
                
                # Find comment box
                comment_box = None
                try:
                    # Method 1: Standard comment textarea
                    comment_box = self.driver.find_element(By.XPATH, "//textarea[@placeholder='Add a comment...' or @aria-label='Add a comment...']")
                except:
                    try:
                        # Method 2: Alternative comment input
                        comment_box = self.driver.find_element(By.XPATH, "//form//textarea")
                    except:
                        try:
                            # Method 3: Any comment input field
                            comment_inputs = self.driver.find_elements(By.XPATH, "//textarea | //input[contains(@placeholder, 'comment')]")
                            if comment_inputs:
                                comment_box = comment_inputs[0]
                        except:
                            pass
                
                if comment_box:
                    try:
                        # Scroll to comment box
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", comment_box)
                        self.human_delay(1, 2)
                        
                        # Click and type comment
                        comment_box.click()
                        self.human_delay(1, 2)
                        comment_box.send_keys(comment_text)
                        self.human_delay(2, 3)
                        
                        # Find and click post button
                        try:
                            post_button = self.driver.find_element(By.XPATH, "//button[text()='Post' or contains(@aria-label, 'Post')]")
                            post_button.click()
                            logging.info(f"SUCCESS: Added comment '{comment_text}' to @{username}'s post")
                            self.human_delay(2, 4)
                        except:
                            # Try pressing Enter instead
                            from selenium.webdriver.common.keys import Keys
                            comment_box.send_keys(Keys.RETURN)
                            logging.info(f"SUCCESS: Added comment '{comment_text}' to @{username}'s post")
                            self.human_delay(2, 4)
                            
                    except Exception as e:
                        logging.warning(f"Could not add comment to @{username}'s post: {e}")
                else:
                    logging.warning(f"Could not find comment box for @{username}'s post")
            else:
                logging.info(f"Skipped commenting on @{username}'s post (random selection)")
                
        except Exception as e:
            logging.warning(f"Error adding comment to @{username}'s post: {e}")
    
    def go_to_home_and_like_posts(self, num_posts=3):
        """Go to home page and like random posts"""
        try:
            logging.info("Going to Instagram home page for random engagement...")
            
            # Go to home page
            self.driver.get("https://www.instagram.com/")
            self.human_delay(4, 6)
            
            likes_count = 0
            posts_processed = 0
            
            # Scroll and like posts from home feed
            for i in range(num_posts):
                try:
                    # Find posts in the feed
                    feed_posts = self.driver.find_elements(By.XPATH, "//article//button[.//svg[@aria-label='Like']]")
                    
                    if feed_posts and posts_processed < len(feed_posts):
                        post = feed_posts[posts_processed]
                        
                        try:
                            # Scroll to post
                            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", post)
                            self.human_delay(2, 3)
                            
                            # Check if already liked
                            try:
                                unlike_button = post.find_element(By.XPATH, ".//svg[@aria-label='Unlike']")
                                logging.info(f"Home post {i+1} already liked - skipping")
                                posts_processed += 1
                                continue
                            except:
                                pass
                            
                            # Click like button
                            post.click()
                            likes_count += 1
                            logging.info(f"SUCCESS: Liked home feed post {i+1}")
                            
                            # Random chance to add comment
                            if random.random() < 0.3:  # 30% chance for home posts
                                self.add_comment_to_post("home_feed")
                            
                            self.human_delay(4, 7)
                            posts_processed += 1
                            
                        except Exception as e:
                            logging.warning(f"Could not like home post {i+1}: {e}")
                            posts_processed += 1
                            continue
                    else:
                        # Scroll down to load more posts
                        self.driver.execute_script("window.scrollBy(0, 800);")
                        self.human_delay(3, 5)
                        
                except Exception as e:
                    logging.warning(f"Error processing home post {i+1}: {e}")
                    continue
            
            logging.info(f"Home engagement complete: {likes_count} likes")
            return likes_count
            
        except Exception as e:
            logging.error(f"Error during home page engagement: {e}")
            return 0
            
    def check_my_recent_activity(self):
        """Check who has liked or commented on my recent posts and return the favor"""
        try:
            logging.info("Checking recent activity on my posts for reciprocal engagement...")
            
            # Go to my profile first
            self.driver.get("https://www.instagram.com/")
            self.human_delay(3, 5)
            
            # Click on profile icon to go to my profile
            try:
                profile_icon = self.driver.find_element(By.XPATH, "//a[contains(@href, '/') and .//img[@alt] and contains(@href, 'bi.pali8278')]")
                profile_icon.click()
            except:
                # Alternative method - click on account menu
                try:
                    account_menu = self.driver.find_element(By.XPATH, "//div[@role='button']//img[@alt]")
                    account_menu.click()
                    self.human_delay(2, 3)
                    # Click on profile link
                    profile_link = self.driver.find_element(By.XPATH, "//a[contains(text(), 'Profile')]")
                    profile_link.click()
                except:
                    logging.warning("Could not navigate to my profile")
                    return []
            
            self.human_delay(4, 6)
            
            # Get my recent posts (last 2-3 posts)
            recent_engagers = []
            try:
                post_links = self.driver.find_elements(By.XPATH, "//article//a[contains(@href, '/p/')]")[:3]
                
                for i, post_link in enumerate(post_links):
                    try:
                        post_url = post_link.get_attribute('href')
                        logging.info(f"Checking activity on my post {i+1}: {post_url}")
                        
                        # Visit the post
                        self.driver.get(post_url)
                        self.human_delay(3, 5)
                        
                        # Check who liked this post
                        try:
                            # Look for likes count/button
                            likes_button = self.driver.find_element(By.XPATH, "//a[contains(@href, '/liked_by/') or contains(text(), 'like')]")
                            likes_button.click()
                            self.human_delay(3, 4)
                            
                            # Get list of people who liked
                            liker_elements = self.driver.find_elements(By.XPATH, "//div[@role='dialog']//a[contains(@href, '/')]")[:5]  # Get first 5 likers
                            
                            for liker in liker_elements:
                                try:
                                    username = liker.get_attribute('href').split('/')[-2]
                                    if username and username not in recent_engagers and username != 'bi.pali8278':
                                        recent_engagers.append(username)
                                        logging.info(f"Found recent liker: @{username}")
                                except:
                                    continue
                            
                            # Close likes dialog
                            self.close_modal()
                            
                        except Exception as e:
                            logging.warning(f"Could not check likes on post {i+1}: {e}")
                        
                        # Check recent comments
                        try:
                            # Look for comment usernames
                            comment_elements = self.driver.find_elements(By.XPATH, "//article//div//a[contains(@href, '/') and not(contains(@href, '/p/'))]")[:5]
                            
                            for commenter in comment_elements:
                                try:
                                    username = commenter.get_attribute('href').split('/')[-2]
                                    if username and username not in recent_engagers and username != 'bi.pali8278':
                                        recent_engagers.append(username)
                                        logging.info(f"Found recent commenter: @{username}")
                                except:
                                    continue
                                    
                        except Exception as e:
                            logging.warning(f"Could not check comments on post {i+1}: {e}")
                        
                        # Limit to avoid too many reciprocal actions
                        if len(recent_engagers) >= 5:
                            break
                            
                    except Exception as e:
                        logging.warning(f"Error processing my post {i+1}: {e}")
                        continue
                        
            except Exception as e:
                logging.warning(f"Could not find my recent posts: {e}")
            
            # Remove duplicates and limit
            recent_engagers = list(dict.fromkeys(recent_engagers))[:5]
            logging.info(f"Found {len(recent_engagers)} users for reciprocal engagement: {recent_engagers}")
            
            return recent_engagers
            
        except Exception as e:
            logging.error(f"Error checking my recent activity: {e}")
            return []
            
    def reciprocal_engagement(self, username):
        """Visit someone's profile and like + comment on one random post as reciprocal engagement"""
        try:
            logging.info(f"Starting reciprocal engagement with @{username}")
            
            if not self.visit_profile(username):
                return False
                
            self.human_delay(3, 5)
            
            # Find their posts
            post_links = []
            try:
                post_elements = self.driver.find_elements(By.XPATH, "//article//a[contains(@href, '/p/')]")
                for element in post_elements[:5]:  # Check first 5 posts
                    href = element.get_attribute('href')
                    if href and '/p/' in href:
                        post_links.append(href)
            except:
                pass
            
            if not post_links:
                logging.warning(f"No posts found for reciprocal engagement with @{username}")
                return False
            
            # Pick a random post
            selected_post = random.choice(post_links)
            logging.info(f"Selected random post for reciprocal engagement: {selected_post}")
            
            # Visit the selected post
            self.driver.get(selected_post)
            self.human_delay(4, 6)
            
            # Like the post
            liked = False
            try:
                # Check if already liked
                unlike_buttons = self.driver.find_elements(By.XPATH, "//button//svg[@aria-label='Unlike']")
                if unlike_buttons:
                    logging.info(f"Post by @{username} already liked")
                    liked = True
                else:
                    # Find and click like button
                    like_buttons = self.driver.find_elements(By.XPATH, "//button[.//svg[@aria-label='Like']]")
                    if like_buttons:
                        like_buttons[0].click()
                        liked = True
                        logging.info(f"SUCCESS: Liked @{username}'s post as reciprocal engagement")
                        self.human_delay(2, 3)
            except Exception as e:
                logging.warning(f"Could not like @{username}'s post: {e}")
            
            # Add comment
            commented = False
            try:
                # Reciprocal engagement comments (more personal)
                reciprocal_comments = [
                    "Thanks for the support! 🙏", "Appreciate you! ❤️", "Great content! 👍", 
                    "Love this! 😍", "Amazing work! 🔥", "Keep it up! 💪", "Awesome! ✨",
                    "So good! 👌", "Perfect! 💯", "Nice one! 🚀"
                ]
                
                comment_text = random.choice(reciprocal_comments)
                
                # Find comment box
                comment_box = self.driver.find_element(By.XPATH, "//textarea[@placeholder='Add a comment...' or @aria-label='Add a comment...']")
                comment_box.click()
                self.human_delay(1, 2)
                comment_box.send_keys(comment_text)
                self.human_delay(2, 3)
                
                # Post comment
                try:
                    post_button = self.driver.find_element(By.XPATH, "//button[text()='Post' or contains(@aria-label, 'Post')]")
                    post_button.click()
                    commented = True
                    logging.info(f"SUCCESS: Added reciprocal comment '{comment_text}' to @{username}'s post")
                except:
                    from selenium.webdriver.common.keys import Keys
                    comment_box.send_keys(Keys.RETURN)
                    commented = True
                    logging.info(f"SUCCESS: Added reciprocal comment '{comment_text}' to @{username}'s post")
                    
                self.human_delay(3, 5)
                
            except Exception as e:
                logging.warning(f"Could not comment on @{username}'s post: {e}")
            
            if liked or commented:
                logging.info(f"RECIPROCAL SUCCESS: Engaged with @{username} (liked: {liked}, commented: {commented})")
                return True
            else:
                logging.warning(f"Could not perform reciprocal engagement with @{username}")
                return False
                
        except Exception as e:
            logging.error(f"Error in reciprocal engagement with @{username}: {e}")
            return False
            
    def check_connection_and_restart_if_needed(self):
        """Check if Instagram connection is still active and restart if needed"""
        try:
            # Try to access Instagram homepage to check connection
            current_url = self.driver.current_url
            if "instagram.com" not in current_url:
                logging.warning("⚠️ Not on Instagram, navigating back...")
                self.driver.get("https://www.instagram.com/")
                self.human_delay(3, 5)
            
            # Check if we're still logged in by looking for user interface elements
            try:
                # Look for home, search, or profile icons that indicate we're logged in
                logged_in_indicators = [
                    "//a[@aria-label='Home']",
                    "//a[contains(@href, '/') and .//svg]",
                    "//button[contains(@aria-label, 'New post')]"
                ]
                
                for indicator in logged_in_indicators:
                    if self.driver.find_elements(By.XPATH, indicator):
                        return True
                        
                # If no indicators found, we might be logged out
                logging.warning("⚠️ Login indicators not found, might be logged out")
                return False
                
            except Exception as e:
                logging.warning(f"⚠️ Could not verify login status: {e}")
                return False
                
        except Exception as e:
            logging.error(f"❌ Connection check failed: {e}")
            return False
            
    def is_browser_alive(self):
        """Check if the browser is still alive and responsive"""
        try:
            # Try a simple operation to check if browser is responsive
            self.driver.current_url
            return True
        except Exception as e:
            error_msg = str(e).lower()
            if any(term in error_msg for term in ['invalid session', 'session deleted', 'disconnected', 'connection']):
                logging.error(f"🔥 Browser crashed or disconnected: {e}")
                return False
            else:
                logging.warning(f"Browser check failed but might be recoverable: {e}")
                return True
    
    def restart_browser_if_needed(self, headless=False):
        """Restart the browser if it has crashed"""
        try:
            if not self.is_browser_alive():
                logging.info("🔄 Restarting browser after crash...")
                if self.driver:
                    try:
                        self.driver.quit()
                    except:
                        pass
                
                # Wait a moment before restart
                time.sleep(5)
                
                # Setup driver again
                self.setup_driver(headless)
                logging.info("✅ Browser restarted successfully")
                return True
            return False
        except Exception as e:
            logging.error(f"❌ Failed to restart browser: {e}")
            return False
            
    def safe_operation(self, operation_func, operation_name, *args, **kwargs):
        """Safely execute an operation with error handling and restart capability"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Check if browser is alive before operation
                if not self.is_browser_alive():
                    logging.warning(f"🔄 Browser not responding, restarting...")
                    headless = os.environ.get("RENDER_DEPLOYMENT", "false").lower() == "true"
                    if self.restart_browser_if_needed(headless):
                        # Re-login after restart
                        if not self.login():
                            logging.error("❌ Could not login after browser restart")
                            continue
                
                # Execute the operation
                return operation_func(*args, **kwargs)
                
            except Exception as e:
                error_msg = str(e).lower()
                if any(term in error_msg for term in ['invalid session', 'session deleted', 'disconnected']):
                    logging.warning(f"🔥 Browser crash detected during {operation_name}: {e}")
                    headless = os.environ.get("RENDER_DEPLOYMENT", "false").lower() == "true"
                    if self.restart_browser_if_needed(headless):
                        # Re-login after restart
                        if not self.login():
                            logging.error("❌ Could not login after browser restart")
                            continue
                    else:
                        logging.error(f"❌ Could not restart browser after crash")
                        break
                else:
                    logging.warning(f"⚠️ {operation_name} failed (attempt {attempt + 1}/{max_retries}): {e}")
                    if attempt < max_retries - 1:
                        # Wait before retry
                        wait_time = (attempt + 1) * 30  # 30, 60, 90 seconds
                        logging.info(f"⏰ Waiting {wait_time} seconds before retry...")
                        time.sleep(wait_time)
                    else:
                        logging.error(f"❌ {operation_name} failed after {max_retries} attempts")
                        return None
                        
        return None
        
    def run_continuous_campaign(self, target_accounts, max_follows_per_cycle=3):
        """Run a continuous 24/7 Instagram automation campaign"""
        cycle_count = 0
        total_follows = 0
        total_likes = 0
        total_reciprocal = 0
        
        logging.info("🔄 STARTING 24/7 CONTINUOUS INSTAGRAM AUTOMATION")
        logging.info(f"Target accounts: {target_accounts}")
        logging.info(f"Max follows per cycle: {max_follows_per_cycle}")
        
        try:
            while True:  # Infinite loop for 24/7 operation
                cycle_count += 1
                logging.info(f"🔄 === CYCLE #{cycle_count} STARTING ===")
                
                # STEP 1: Check for reciprocal engagement opportunities
                logging.info("🤝 === CHECKING FOR RECIPROCAL ENGAGEMENT ===")
                reciprocal_count = 0
                try:
                    recent_engagers = self.safe_operation(self.check_my_recent_activity, "reciprocal engagement check")
                    
                    if recent_engagers:
                        logging.info(f"Found {len(recent_engagers)} users for reciprocal engagement")
                        for engager in recent_engagers[:2]:  # Limit to 2 per cycle for continuous operation
                            try:
                                result = self.safe_operation(self.reciprocal_engagement, "reciprocal engagement", engager)
                                if result:
                                    reciprocal_count += 1
                                    total_reciprocal += 1
                                    # Human-like delay between reciprocal engagements
                                    delay = random.uniform(20, 35)
                                    logging.info(f"⏰ Waiting {delay:.1f} seconds before next reciprocal engagement...")
                                    time.sleep(delay)
                            except Exception as e:
                                logging.warning(f"Error in reciprocal engagement with @{engager}: {e}")
                    else:
                        logging.info("No recent engagers found")
                        
                except Exception as e:
                    logging.warning(f"⚠️ Reciprocal engagement check failed: {e}")
                
                # STEP 3: Regular follow campaign (rotate through target accounts)
                logging.info("👥 === STARTING FOLLOW CAMPAIGN ===")
                follows_this_cycle = 0
                likes_this_cycle = 0
                
                # Use modulo to cycle through target accounts
                target_index = (cycle_count - 1) % len(target_accounts)
                current_target = target_accounts[target_index]
                
                logging.info(f"🎯 Processing target account: @{current_target} (Account {target_index + 1}/{len(target_accounts)})")
                
                try:
                    if self.visit_profile(current_target):
                        followers = self.get_followers_list(max_followers=20)  # Increased for fast sessions
                        
                        if followers:
                            for follower in followers:
                                if follows_this_cycle >= max_follows_per_cycle:
                                    break
                                    
                                # Increased engagement probability for fast sessions
                                if random.random() < 0.8:  # 80% chance for fast acquisition
                                    logging.info(f"🔗 Engaging with @{follower}")
                                    
                                    try:
                                        followed = self.follow_user(follower)
                                        if followed:
                                            follows_this_cycle += 1
                                            total_follows += 1
                                            
                                        # Try to like posts
                                        post_likes = self.like_recent_posts(follower, max_likes=1)
                                        likes_this_cycle += post_likes
                                        total_likes += post_likes
                                        
                                        # Delay between users (Fast timing for 15 followers in 15 minutes)
                                        delay = random.uniform(45, 75)  # 45-75 seconds: 1 follower per minute
                                        logging.info(f"⏰ Waiting {delay:.1f} seconds before next user...")
                                        time.sleep(delay)
                                        
                                    except Exception as e:
                                        logging.warning(f"Error engaging with @{follower}: {e}")
                                else:
                                    logging.info(f"⏭️ Skipped @{follower} (random selection)")
                        else:
                            logging.warning(f"No followers found for @{current_target}")
                    else:
                        logging.warning(f"Could not visit @{current_target}")
                        
                except Exception as e:
                    logging.warning(f"Error in follow campaign: {e}")
                
                # STEP 4: Home engagement
                logging.info("🏠 === HOME PAGE ENGAGEMENT ===")
                home_likes = 0
                try:
                    home_likes = self.go_to_home_and_like_posts(random.randint(1, 2))  # Reduced for continuous
                    total_likes += home_likes
                    logging.info(f"✅ Home engagement complete: {home_likes} likes")
                except Exception as e:
                    logging.warning(f"⚠️ Home engagement failed: {e}")
                
                # Cycle summary
                logging.info(f"🔄 === CYCLE #{cycle_count} COMPLETE ===")
                logging.info(f"📊 Cycle Stats: {follows_this_cycle} follows, {likes_this_cycle + home_likes} likes, {reciprocal_count} reciprocal engagements")
                logging.info(f"📈 Total Stats: {total_follows} follows, {total_likes} likes, {total_reciprocal} reciprocal")
                
                # Break between cycles (Fast timing for 15-minute sessions)
                if follows_this_cycle > 0 or reciprocal_count > 0:
                    break_time = random.uniform(60, 120)  # 1-2 minutes between active cycles (Fast)
                    logging.info(f"😴 Taking break for {break_time/60:.1f} minutes before next cycle...")
                else:
                    break_time = random.uniform(30, 60)  # 30 seconds-1 minute for inactive cycles
                    logging.info(f"😴 Taking short break for {break_time/60:.1f} minutes before next cycle...")
                
                time.sleep(break_time)
                
                # Safety check - if too many errors, take longer break
                if cycle_count % 20 == 0:  # Every 20 cycles
                    long_break = random.uniform(300, 600)  # 5-10 minutes
                    logging.info(f"🛌 Taking long safety break for {long_break/60:.1f} minutes after {cycle_count} cycles...")
                    time.sleep(long_break)
                
        except KeyboardInterrupt:
            logging.info("🛑 Continuous campaign stopped by user")
        except Exception as e:
            logging.error(f"❌ Critical error in continuous campaign: {e}")
            # Wait before potential restart
            time.sleep(300)  # 5 minutes
            
        finally:
            logging.info(f"🏁 CONTINUOUS CAMPAIGN ENDED AFTER {cycle_count} CYCLES")
            logging.info(f"📊 FINAL STATS: {total_follows} total follows, {total_likes} total likes, {total_reciprocal} reciprocal engagements")
            
    def run_follow_campaign(self, target_accounts, max_follows=5):
        """Run an enhanced follow campaign with reciprocal engagement, auto-reply, and home engagement"""
        total_follows = 0
        total_likes = 0
        home_likes = 0
        actual_follows = 0  # Track actual new follows (not already following)
        reciprocal_engagements = 0
        
        # FIRST: Check for reciprocal engagement opportunities
        logging.info("=== CHECKING FOR RECIPROCAL ENGAGEMENT OPPORTUNITIES ===")
        recent_engagers = self.check_my_recent_activity()
        
        if recent_engagers:
            logging.info(f"Found {len(recent_engagers)} users for reciprocal engagement")
            for engager in recent_engagers[:3]:  # Limit to 3 reciprocal engagements
                try:
                    if self.reciprocal_engagement(engager):
                        reciprocal_engagements += 1
                        # Human-like delay between reciprocal engagements
                        delay = random.uniform(25, 45)
                        logging.info(f"Waiting {delay:.1f} seconds before next reciprocal engagement...")
                        time.sleep(delay)
                except Exception as e:
                    logging.warning(f"Error in reciprocal engagement with @{engager}: {e}")
        else:
            logging.info("No recent engagers found for reciprocal engagement")
        
        # THIRD: Continue with regular campaign
        logging.info("=== STARTING REGULAR FOLLOW CAMPAIGN ===")
        
        for target_account in target_accounts:
            if actual_follows >= max_follows:
                break
                
            logging.info(f"Processing target account: @{target_account}")
            
            # Get followers from target account
            if self.visit_profile(target_account):
                followers = self.get_followers_list(max_followers=8)  # Reduced number
                
                if not followers:
                    logging.warning(f"No followers found for @{target_account}, trying direct engagement")
                    # If we can't get followers, try to like posts from the target account itself
                    likes = self.like_recent_posts(target_account, max_likes=1)
                    total_likes += likes
                    continue
                
                for follower in followers:
                    if actual_follows >= max_follows:
                        break
                        
                    # Randomly decide to engage (not every follower)
                    if random.random() < 0.6:  # 60% chance (reduced from 70%)
                        logging.info(f"Engaging with @{follower}")
                        
                        # Try to follow the user first
                        follow_result = self.follow_user(follower)
                        
                        if follow_result == "already_following":
                            logging.info(f"Already following @{follower} - moving to next user")
                            continue  # Skip to next user
                        elif follow_result == True:
                            actual_follows += 1
                            total_follows += 1
                            logging.info(f"SUCCESS: Followed @{follower} (New follow #{actual_follows})")
                        
                        # Then try to like posts (if available)
                        likes = self.like_recent_posts(follower, max_likes=1)
                        total_likes += likes
                        
                        if follow_result or likes > 0:
                            logging.info(f"Successfully engaged with @{follower} (followed: {follow_result}, likes: {likes})")
                        else:
                            logging.info(f"Could not engage with @{follower}")
                        
                        # After every 3-4 follows, go to home page for random engagement
                        if actual_follows > 0 and actual_follows % random.randint(3, 4) == 0:
                            logging.info(f"Taking break for home page engagement after {actual_follows} follows...")
                            home_engagement = self.go_to_home_and_like_posts(random.randint(2, 4))
                            home_likes += home_engagement
                            
                            # Longer break after home engagement
                            delay = random.uniform(45, 90)
                            logging.info(f"Resting for {delay:.1f} seconds after home engagement...")
                            time.sleep(delay)
                        
                        # Long delay between users (Fast for 15 followers in 15 minutes)
                        delay = random.uniform(45, 75)  # 45-75 seconds (Fast)
                        logging.info(f"Waiting {delay:.1f} seconds before next user...")
                        time.sleep(delay)
                    else:
                        logging.info(f"Skipped @{follower} (random selection)")
                        
            # Break between target accounts
            if target_account != target_accounts[-1] and actual_follows < max_follows:
                break_time = random.uniform(45, 90)  # 45-90 seconds
                logging.info(f"Taking break for {break_time:.1f} seconds between target accounts...")
                time.sleep(break_time)
                
        # Final home engagement if we haven't done it recently
        if actual_follows > 0:
            logging.info("Final home page engagement before ending session...")
            final_home_engagement = self.go_to_home_and_like_posts(random.randint(2, 3))
            home_likes += final_home_engagement
                
        logging.info(f"Campaign complete: {reciprocal_engagements} reciprocal engagements, {actual_follows} new follows, {total_likes} profile likes, {home_likes} home likes")
        return actual_follows, total_likes + home_likes, reciprocal_engagements
        
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            
def main_with_restart():
    """Main function with automatic restart capability"""
    restart_count = 0
    max_restarts = 10  # Increased for handling Chrome crashes
    
    while restart_count < max_restarts:
        try:
            logging.info(f"🔄 Starting bot (Restart #{restart_count})")
            main()
            # If main() completes normally, break the loop
            break
            
        except KeyboardInterrupt:
            logging.info("🛑 Bot stopped by user")
            break
            
        except Exception as e:
            restart_count += 1
            error_msg = str(e).lower()
            
            # Check if it's a browser crash
            if any(term in error_msg for term in ['invalid session', 'session deleted', 'disconnected', 'chrome']):
                logging.error(f"� Browser crash detected: {e}")
                wait_time = 30  # Quick restart for browser crashes
            else:
                logging.error(f"💥 Bot crashed: {e}")
                wait_time = restart_count * 60  # Progressive delay for other errors
            
            if restart_count < max_restarts:
                logging.info(f"🔄 Restarting in {wait_time//60} minutes... (Restart {restart_count}/{max_restarts})")
                time.sleep(wait_time)
            else:
                logging.error(f"❌ Maximum restarts ({max_restarts}) reached. Stopping bot.")
                break

def main():
    # Configuration - Get credentials from environment variables
    USERNAME = os.environ.get("INSTAGRAM_USERNAME")
    PASSWORD = os.environ.get("INSTAGRAM_PASSWORD")
    
    # Check if credentials are provided
    if not USERNAME or not PASSWORD:
        logging.error("❌ Missing credentials! Please set INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD environment variables")
        logging.error("💡 Example: export INSTAGRAM_USERNAME='your_email@gmail.com'")
        logging.error("💡 Example: export INSTAGRAM_PASSWORD='your_password'")
        return
    
    TARGET_ACCOUNTS = [
        "lavanya.das_",
        "shreeyasatapathy", 
        "bashu_sanchita"
    ]  # Added new influencers
    MAX_FOLLOWS_PER_CYCLE = 15  # Fast: 15 followers in 15 minutes
    
    # HEADLESS MODE CONTROL - True for Render deployment, False for local debugging
    HEADLESS_MODE = os.environ.get("RENDER_DEPLOYMENT", "false").lower() == "true"
    
    bot = None
    try:
        if HEADLESS_MODE:
            logging.info("🚀 === STARTING 24/7 HEADLESS BOT WITH SESSION PERSISTENCE ===")
            logging.info("🔄 Using Chrome profile for persistent login (reduces Instagram challenges)")
        else:
            logging.info("🚀 === STARTING 24/7 VISUAL BOT WITH SESSION PERSISTENCE ===")
        
        # Create bot instance with session persistence
        bot = InstagramWebBot(USERNAME, PASSWORD, headless=HEADLESS_MODE)
        
        # Login (will check for existing session first)
        if bot.login():
            logging.info("🎯 Session ready - starting continuous automation")
            # Run continuous 24/7 campaign
            bot.run_continuous_campaign(TARGET_ACCOUNTS, MAX_FOLLOWS_PER_CYCLE)
        else:
            logging.error("❌ Login failed even with session persistence")
            
    except Exception as e:
        logging.exception(f"💥 Bot error: {e}")
        raise  # Re-raise to trigger restart
    finally:
        if bot:
            # Don't clear session data on close - keep it for next run
            logging.info("💾 Preserving session data for next run")
            bot.close()
            
if __name__ == "__main__":
    main_with_restart()

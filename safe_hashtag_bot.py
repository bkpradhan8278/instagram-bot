import time
import random
import json
import os
import logging
from datetime import datetime, timedelta
from instagrapi import Client

# ---------------------------
# CONFIG (edit these safely)
# ---------------------------
USERNAME = "bi.pali8278@gmail.com"
PASSWORD = "Bk8278@@"
SESSION_FILE = "session.json"
LOG_FILE = "ig_bot_hashtag_only.log"

COMMENTS = [
    "Awesome post! 🔥",
    "Love this — keep it up! 🙌", 
    "Nice shot! ✨",
    "This is great — saved! 💾",
    "Amazing content! 👏",
    "So inspiring! ✨",
    "Great work! 💪",
    "Beautiful! 😍",
    "Love your style! 💕",
]

HASHTAGS = ["photography", "art", "nature", "travel", "lifestyle"]

# Ultra-conservative limits
MAX_LIKES_PER_RUN = 3
DELAY_BETWEEN_ACTIONS = (120, 300)  # 2-5 minutes between actions

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    filename=LOG_FILE,
    filemode="a",
    format="%(asctime)s | %(levelname)s | %(message)s"
)
console = logging.StreamHandler()
console.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
logging.getLogger().addHandler(console)

cl = Client()
cl.delay_range = [3, 8]  # Very slow API calls

def load_or_login():
    try:
        if os.path.exists(SESSION_FILE):
            cl.load_settings(SESSION_FILE)
            cl.login(USERNAME, PASSWORD)
            cl.dump_settings(SESSION_FILE)
            logging.info("✅ Logged in using saved session.")
            return
    except Exception as e:
        logging.warning("Saved session load failed: %s", e)

    try:
        cl.login(USERNAME, PASSWORD)
        cl.dump_settings(SESSION_FILE)
        logging.info("✅ Logged in and saved new session.")
    except Exception as e:
        logging.exception("❌ Login failed.")
        raise

def safe_hashtag_activity():
    logging.info("Starting SAFE hashtag activity...")
    likes_count = 0
    
    for tag in random.sample(HASHTAGS, min(2, len(HASHTAGS))):  # Only 2 random hashtags
        try:
            logging.info(f"Browsing #{tag}")
            medias = cl.hashtag_medias_v1(tag, amount=2, tab_key="recent")
            
            for media in medias:
                if likes_count >= MAX_LIKES_PER_RUN:
                    logging.info("Reached like limit.")
                    return
                    
                # Only like 50% of posts (more selective)
                if random.random() < 0.5:
                    try:
                        cl.media_like(media.id)
                        likes_count += 1
                        logging.info(f"✅ Liked post by @{media.user.username} for #{tag}")
                        
                        # Long delay between likes
                        delay = random.uniform(*DELAY_BETWEEN_ACTIONS)
                        logging.info(f"Waiting {delay/60:.1f} minutes before next action...")
                        time.sleep(delay)
                        
                    except Exception as e:
                        logging.warning(f"Failed to like post: {e}")
                        break
                else:
                    logging.info(f"Viewed but didn't like post by @{media.user.username}")
                    time.sleep(random.uniform(30, 90))  # Short viewing delay
                    
        except Exception as e:
            logging.warning(f"Error with hashtag #{tag}: {e}")
            
    logging.info(f"✅ Safe run complete. Total likes: {likes_count}")

def main():
    logging.info("=== STARTING SAFE HASHTAG-ONLY BOT ===")
    
    try:
        load_or_login()
        
        # Initial delay
        initial_delay = random.uniform(120, 300)
        logging.info(f"Starting with delay of {initial_delay/60:.1f} minutes")
        time.sleep(initial_delay)
        
        safe_hashtag_activity()
        
    except Exception as e:
        logging.exception("Bot error: %s", e)
    finally:
        try:
            cl.logout()
            logging.info("Logged out cleanly.")
        except Exception:
            pass

if __name__ == "__main__":
    main()

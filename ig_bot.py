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
LOG_FILE = "ig_bot.log"

# Influencers to source followers from (no duplicates)
INDIAN_INFLUENCERS = [
    "udayanonmoney",
    "lavanya.das_",
    "shreeyasatapathy",
    "bashu_sanchita"
    # "chahalvermaa",  # This one was causing issues
]

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
    "Incredible! 🔥",
    "Keep shining! ⭐",
    "Perfect! 👌",
    "Outstanding! 🙌",
    "Brilliant! 💎",
    "Stunning! 😊"
]

HASHTAGS = ["technology", "fashion", "photography", "art", "nature"]
TARGET_ACCOUNTS_FOR_DM = []  # Leave empty or set targets. DMing is OFF by default.
DM_MESSAGE = "Hey! I love your content. Let's connect. 🚀"

# Safety controls - ULTRA CONSERVATIVE to avoid detection
FOLLOWER_THRESHOLD = 500          # only follow users with < this many followers
MAX_FOLLOWS_PER_RUN = 2           # ULTRA REDUCED: only 2 follows per run
MAX_LIKES_PER_RUN = 5             # ULTRA REDUCED: only 5 likes per run
MAX_DMS_PER_RUN = 0               # DISABLED: no DMs
ENABLE_DMS = False                # default OFF (change to True with caution)
MAX_ERRORS_BEFORE_PAUSE = 1       # ULTRA REDUCED: stop immediately on errors

# Rate-limiting window (simple per-hour limiter)
HOUR_WINDOW = timedelta(hours=1)

# Anti-detection delays (seconds) - ULTRA INCREASED for stealth
DELAY_BETWEEN_ACTIONS = (180, 600)   # ULTRA INCREASED: 3-10 minutes between actions
DELAY_AFTER_USER = (600, 1800)       # ULTRA INCREASED: 10-30 minutes after each user
DELAY_BETWEEN_SESSIONS = (7200, 14400) # ULTRA INCREASED: 2-4 hour breaks between bot runs
HUMAN_LIKE_VARIANCE = (10, 60)       # INCREASED: 10-60 second micro-delays

# ---------------------------
# Setup logging & client
# ---------------------------
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

# Anti-detection settings for client
cl.delay_range = [1, 3]  # Random delays between API calls

def load_or_login():
    """Try to reuse saved session; otherwise login and save session."""
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

# ---------------------------
# Rate limiter / counters
# ---------------------------
class ActionLimiter:
    def __init__(self):
        self.window_start = datetime.utcnow()
        self.follows = 0
        self.likes = 0
        self.dms = 0

    def reset_if_needed(self):
        if datetime.utcnow() - self.window_start > HOUR_WINDOW:
            logging.info("Resetting hourly counters.")
            self.window_start = datetime.utcnow()
            self.follows = 0
            self.likes = 0
            self.dms = 0

    def can_follow(self):
        self.reset_if_needed()
        return self.follows < MAX_FOLLOWS_PER_RUN

    def can_like(self):
        self.reset_if_needed()
        return self.likes < MAX_LIKES_PER_RUN

    def can_dm(self):
        self.reset_if_needed()
        return ENABLE_DMS and (self.dms < MAX_DMS_PER_RUN)

limiter = ActionLimiter()

# ---------------------------
# Utility helpers
# ---------------------------
def rand_sleep(rng):
    s = random.uniform(*rng)
    logging.debug("Sleeping for %.1f seconds", s)
    time.sleep(s)

def human_like_delay():
    """Add small random delays to mimic human behavior"""
    s = random.uniform(*HUMAN_LIKE_VARIANCE)
    time.sleep(s)

def should_take_break():
    """Randomly decide if bot should take a longer break (simulating human fatigue)"""
    return random.random() < 0.15  # 15% chance to take a break

def weekend_slowdown():
    """Slow down activity on weekends like humans do"""
    now = datetime.now()
    if now.weekday() >= 5:  # Saturday = 5, Sunday = 6
        return random.uniform(1.5, 2.5)  # 150-250% slower on weekends
    return 1.0

def safe_call(func, *args, backoff_base=2, max_tries=4, **kwargs):
    """Call func with retries and exponential backoff on exceptions."""
    tries = 0
    while True:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            tries += 1
            logging.warning("Call failed (%d/%d): %s", tries, max_tries, e)
            if tries >= max_tries:
                logging.error("Max retries reached for function %s", func.__name__)
                raise
            backoff = backoff_base ** tries + random.uniform(1, 3)
            logging.info("Backing off for %.1f sec", backoff)
            time.sleep(backoff)

# ---------------------------
# Core actions
# ---------------------------
def engage_and_follow(user_id):
    """Like + comment on recent posts then follow the user (if allowed)."""
    try:
        # Add human-like delay before checking user
        human_like_delay()
        full_info = safe_call(cl.user_info, user_id)
    except Exception as e:
        logging.warning("Could not fetch user info for %s: %s", user_id, e)
        return False

    if full_info.is_private:
        logging.info("Skipping private account: %s", full_info.username)
        return False
    if full_info.username == USERNAME:
        return False

    if full_info.follower_count >= FOLLOWER_THRESHOLD:
        logging.info("Skipping %s — has %d followers (>= threshold)", full_info.username, full_info.follower_count)
        return False

    # Skip verified accounts (they're monitored more closely)
    if hasattr(full_info, 'is_verified') and full_info.is_verified:
        logging.info("Skipping verified account: %s", full_info.username)
        return False

    # Fetch up to 2 recent medias
    try:
        medias = safe_call(cl.user_medias_v1, user_id, amount=2)
    except Exception as e:
        logging.warning("No medias or failed to fetch medias for %s: %s", full_info.username, e)
        medias = []

    # Don't always like/comment - sometimes just view (more human-like)
    should_engage = random.random() < 0.7  # 70% chance to engage
    
    for media in medias:
        if not limiter.can_like():
            logging.info("Hit likes/hour limit. Skipping further likes.")
            break
            
        # Add viewing time (humans don't instantly like)
        human_like_delay()
        
        if should_engage:
            try:
                safe_call(cl.media_like, media.id)
                limiter.likes += 1
                
                # Only comment sometimes (not every like)
                if random.random() < 0.4:  # 40% chance to comment after like
                    comment = random.choice(COMMENTS)
                    safe_call(cl.media_comment, media.id, comment)
                    logging.info("Liked & commented on @%s: '%s'", full_info.username, comment)
                else:
                    logging.info("Liked post by @%s", full_info.username)
                    
            except Exception as e:
                logging.warning("Engagement error for %s: %s", full_info.username, e)
        else:
            logging.info("Viewed but didn't engage with @%s (human-like behavior)", full_info.username)
            
        # Apply weekend slowdown factor
        delay_multiplier = weekend_slowdown()
        adjusted_delay = (DELAY_BETWEEN_ACTIONS[0] * delay_multiplier, 
                         DELAY_BETWEEN_ACTIONS[1] * delay_multiplier)
        rand_sleep(adjusted_delay)

    # Follow (if still allowed and sometimes skip to be more human-like)
    should_follow = random.random() < 0.8  # 80% chance to follow after engagement
    
    if limiter.can_follow() and should_follow:
        try:
            safe_call(cl.user_follow, user_id)
            limiter.follows += 1
            logging.info("Followed @%s", full_info.username)
            
            # Apply weekend slowdown factor
            delay_multiplier = weekend_slowdown()
            adjusted_delay = (DELAY_AFTER_USER[0] * delay_multiplier,
                             DELAY_AFTER_USER[1] * delay_multiplier)
            rand_sleep(adjusted_delay)
            return True
        except Exception as e:
            logging.warning("Failed to follow %s: %s", full_info.username, e)
            return False
    else:
        if not limiter.can_follow():
            logging.info("Hit follows/hour or per-run limit; not following more.")
        else:
            logging.info("Chose not to follow @%s (human-like behavior)", full_info.username)
        return False

def follow_new_accounts_of_influencers():
    logging.info("Starting follower-sourcing routine.")
    error_count = 0

    for influencer in INDIAN_INFLUENCERS:
        if limiter.follows >= MAX_FOLLOWS_PER_RUN:
            logging.info("Reached follow cap for this run.")
            break

        # Random break between influencers (simulate human browsing)
        if should_take_break():
            break_time = random.uniform(300, 900)  # 5-15 minute break
            logging.info("Taking a human-like break for %.1f minutes", break_time/60)
            time.sleep(break_time)

        try:
            influencer_info = safe_call(cl.user_info_by_username, influencer)
            # Reduce amount to be less suspicious
            amount = random.randint(10, 25)  # Random between 10-25 instead of fixed 50
            followers = safe_call(cl.user_followers, influencer_info.pk, amount=amount)
            logging.info("Fetched %d followers for %s", len(followers), influencer)
        except Exception as e:
            logging.warning("Skipping influencer %s due to error: %s", influencer, e)
            error_count += 1
            if error_count >= MAX_ERRORS_BEFORE_PAUSE:
                logging.warning("Too many errors — pausing run.")
                break
            continue

        # Randomize order of followers (don't always start from top)
        follower_items = list(followers.items())
        random.shuffle(follower_items)

        # iterate followers (dict: id -> user)
        for uid, uinfo in follower_items:
            if limiter.follows >= MAX_FOLLOWS_PER_RUN:
                logging.info("Reached follow cap for this run.")
                return
            try:
                success = engage_and_follow(uid)
                if success:
                    logging.info("Engaged+followed %s", uinfo.username)
                
                # Random pacing with human-like variance
                base_delay = random.uniform(30, 90)
                delay_multiplier = weekend_slowdown()
                final_delay = base_delay * delay_multiplier
                time.sleep(final_delay)
                
            except Exception as e:
                logging.warning("Error processing follower %s: %s", uinfo.username if hasattr(uinfo, "username") else uid, e)
                error_count += 1
                if error_count >= MAX_ERRORS_BEFORE_PAUSE:
                    logging.warning("Too many errors — pausing run.")
                    return

def auto_like_by_hashtags():
    logging.info("Starting hashtag auto-like routine.")
    
    # Shuffle hashtags to avoid predictable patterns
    shuffled_tags = HASHTAGS.copy()
    random.shuffle(shuffled_tags)
    
    for tag in shuffled_tags:
        # Random break chance
        if should_take_break():
            break_time = random.uniform(180, 600)  # 3-10 minute break
            logging.info("Taking a break for %.1f minutes", break_time/60)
            time.sleep(break_time)
            
        try:
            # Reduce amount and randomize
            amount = random.randint(2, 4)  # Much smaller amounts
            medias = safe_call(cl.hashtag_medias_v1, tag, amount=amount, tab_key="recent")
            
            for media in medias:
                if not limiter.can_like():
                    logging.info("Reached likes cap.")
                    return
                    
                # Don't like every post - be selective like humans
                if random.random() < 0.6:  # 60% chance to like
                    safe_call(cl.media_like, media.id)
                    limiter.likes += 1
                    logging.info("Liked post by @%s for #%s", media.user.username, tag)
                else:
                    logging.info("Viewed but didn't like post by @%s for #%s", media.user.username, tag)
                
                # Apply weekend slowdown
                delay_multiplier = weekend_slowdown()
                adjusted_delay = (DELAY_BETWEEN_ACTIONS[0] * delay_multiplier,
                                 DELAY_BETWEEN_ACTIONS[1] * delay_multiplier)
                rand_sleep(adjusted_delay)
                
        except Exception as e:
            logging.warning("Error fetching/liking for #%s: %s", tag, e)

def auto_dm_followers_of_targets():
    if not ENABLE_DMS or not TARGET_ACCOUNTS_FOR_DM:
        logging.info("DMs are disabled or no target accounts set. Skipping DMs.")
        return

    logging.info("Starting auto-DM routine.")
    for target in TARGET_ACCOUNTS_FOR_DM:
        try:
            target_info = safe_call(cl.user_info_by_username, target)
            followers = safe_call(cl.user_followers, target_info.pk, amount=10)
            for uid, uinfo in followers.items():
                if not limiter.can_dm():
                    logging.info("Reached DM cap.")
                    return
                try:
                    safe_call(cl.direct_send, DM_MESSAGE, [uid])
                    limiter.dms += 1
                    logging.info("Sent DM to @%s", uinfo.username)
                    rand_sleep(DELAY_BETWEEN_ACTIONS)
                except Exception as e:
                    logging.warning("Failed to send DM to %s: %s", uinfo.username, e)
        except Exception as e:
            logging.warning("Skipping DM target %s due to error: %s", target, e)

# ---------------------------
# Main runner
# ---------------------------
def main():
    logging.info("=== STARTING BOT RUN ===")
    
    # Check if it's a reasonable time to be active (avoid 2-6 AM)
    current_hour = datetime.now().hour
    if 2 <= current_hour <= 6:
        logging.info("It's late night/early morning. Humans usually sleep. Skipping run.")
        return
    
    load_or_login()

    try:
        # Add initial random delay (humans don't start immediately)
        initial_delay = random.uniform(60, 300)  # 1-5 minutes
        logging.info("Starting with human-like delay of %.1f minutes", initial_delay/60)
        time.sleep(initial_delay)
        
        follow_new_accounts_of_influencers()
        
        # Longer, more variable breaks between activities
        break_time = random.uniform(300, 900)  # 5-15 minutes
        logging.info("Taking break for %.1f minutes before next task...", break_time/60)
        time.sleep(break_time)

        auto_like_by_hashtags()
        
        break_time = random.uniform(300, 900)  # 5-15 minutes  
        logging.info("Taking break for %.1f minutes before next task...", break_time/60)
        time.sleep(break_time)

        auto_dm_followers_of_targets()

        logging.info("✅ Run complete. Summary: follows=%d likes=%d dms=%d", limiter.follows, limiter.likes, limiter.dms)
        
        # Random session break before potential next run
        if random.random() < 0.3:  # 30% chance to take long break
            long_break = random.uniform(*DELAY_BETWEEN_SESSIONS)
            logging.info("Taking long session break for %.1f hours", long_break/3600)
            time.sleep(long_break)
            
    except Exception as e:
        logging.exception("Unexpected crash in main: %s", e)
    finally:
        try:
            cl.logout()
            logging.info("Logged out cleanly.")
        except Exception:
            pass

if __name__ == "__main__":
    main()

import time
import random
import json
from instagrapi import Client

# ✅ Instagram Credentials
USERNAME = "bi.pali8278@gmail.com"
PASSWORD = "Tapu8278@"

# ✅ Initialize Instagram Client
cl = Client()

# ✅ Load saved session (to avoid frequent logins)
SESSION_FILE = "session.json"

def login():
    try:
        cl.load_settings(SESSION_FILE)
        cl.login(USERNAME, PASSWORD)
        print("✅ Logged in using saved session.")
    except Exception:
        print("⚠️ Session not found. Logging in manually...")
        cl.login(USERNAME, PASSWORD)
        cl.dump_settings(SESSION_FILE)
        print("✅ New session saved.")

login()

# ✅ Indian Influencers to Extract Followers From
INDIAN_INFLUENCERS = ["mrinmay_ms",
    "sizzlingsoni", "pretty_sheeeee", "mrinmay_ms",
    "lavanya.das_", "shreeyasatapathy", "bashu_sanchita", "zaaliim_queen_mama"
]

COMMENTS = ["Awesome post!", "Great content!", "Love this!"]

# ✅ Function: Randomized Delay
def safe_delay():
    time.sleep(random.uniform(60, 180))  # 1 to 3 minutes

# ✅ Function: Like & Comment Before Following (Exclude Private Accounts)
def engage_and_follow(user_id, username):
    try:
        user_info = cl.user_info(user_id)
        if user_info.is_private:
            print(f"🔒 Skipping {username} (Private Account)")
            return  # Skip private accounts

        medias = cl.user_medias_v1(user_id, amount=2)
        if not medias:
            print(f"⚠️ No recent posts found for {username}. Skipping...")
            return
        
        for media in medias:
            try:
                cl.media_like(media.id)
                comment = random.choice(COMMENTS)
                cl.media_comment(media.id, comment)
                print(f"❤️ Liked & 💬 Commented '{comment}' on {username}'s post")
            except Exception as e:
                print(f"⚠️ Error engaging with {username}: {e}")
            safe_delay()

        cl.user_follow(user_id)
        print(f"✅ Followed {username}")
        safe_delay()
    except Exception as e:
        print(f"⚠️ Error engaging with {username}: {e}")

# ✅ Function: Follow Followers of Indian Influencers (Prioritizing New Accounts)
def follow_new_accounts_of_influencers():
    print("🚀 Searching for new accounts with low followers...")

    for influencer in INDIAN_INFLUENCERS:
        try:
            user_info = cl.user_info_by_username(influencer)
            user_id = user_info.pk  # Get the actual user ID
            
            followers = cl.user_followers(user_id, amount=50)  # Fetch 50 followers per influencer
            
            for user_id, user_info in followers.items():
                full_info = cl.user_info(user_id)  # Fetch full user details
                if full_info.is_private:
                    print(f"🔒 Skipping private account: {full_info.username}")
                    continue
                
                if full_info.follower_count < 5000:  # Only follow users with < 500 followers
                    print(f"✅ Found new account: {full_info.username} ({full_info.follower_count} followers)")
                    engage_and_follow(user_id, full_info.username)
                    
        except Exception as e:
            print(f"⚠️ Error processing followers of {influencer}: {e}")

# ✅ Function: Auto-Like Posts
def auto_like():
    print("🚀 Starting Auto-Like")
    HASHTAGS = ["technology", "fashion", "photography", "art", "nature"]  # Example hashtags
    for hashtag in HASHTAGS:
        try:
            medias = cl.hashtag_medias_v1(hashtag, amount=5, tab_key="recent")
            if not medias:
                print(f"⚠️ No posts found for #{hashtag}. Skipping...")
                continue
            
            for media in medias:
                cl.media_like(media.id)
                print(f"❤️ Liked post by {media.user.username}")
                safe_delay()
        except Exception as e:
            print(f"⚠️ Error processing hashtag {hashtag}: {e}")

# ✅ Function: Auto DM Followers of Target Accounts
def auto_dm():
    print("📩 Sending Direct Messages")
    TARGET_ACCOUNTS = ["elonmusk", "voguemagazine"]  # Example target accounts
    DM_MESSAGE = "Hey! I love your content. Let's connect. 🚀"
    
    for target in TARGET_ACCOUNTS:
        try:
            target_user = cl.user_info_by_username(target)
            target_id = target_user.pk  # Get correct ID
            
            followers = cl.user_followers(target_id, amount=5)
            for user_id, user_info in followers.items():
                cl.direct_send(DM_MESSAGE, [user_id])
                print(f"📩 Sent DM to {user_info.username}")
                safe_delay()
        except Exception as e:
            print(f"⚠️ Error sending DMs to followers of {target}: {e}")

# ✅ Run Functions with Delays
follow_new_accounts_of_influencers()
print("⏳ Waiting 10 minutes before next task...")
time.sleep(600)

auto_like()
print("⏳ Waiting 10 minutes before next task...")
time.sleep(600)

auto_dm()
print("✅ All tasks completed successfully!")

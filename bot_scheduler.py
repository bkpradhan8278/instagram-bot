import random
import time
import subprocess
import logging
from datetime import datetime, timedelta
import sys
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("scheduler.log"),
        logging.StreamHandler()
    ]
)

def is_good_time_to_run():
    """Check if it's a good time for the bot to be active"""
    now = datetime.now()
    hour = now.hour
    
    # Avoid late night/early morning (2-6 AM)
    if 2 <= hour <= 6:
        return False
    
    # Reduce activity on weekends
    if now.weekday() >= 5:  # Weekend
        return random.random() < 0.4  # 40% chance on weekends
    
    return True

def run_bot():
    """Execute the Instagram bot"""
    try:
        logging.info("Starting Instagram bot...")
        result = subprocess.run([sys.executable, "ig_bot.py"], 
                              capture_output=True, text=True, timeout=3600)
        
        if result.returncode == 0:
            logging.info("Bot completed successfully")
        else:
            logging.error(f"Bot failed with return code {result.returncode}")
            logging.error(f"Error output: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        logging.error("Bot timed out after 1 hour")
    except Exception as e:
        logging.error(f"Error running bot: {e}")

def main():
    """Main scheduler loop"""
    logging.info("Starting Instagram bot scheduler...")
    
    while True:
        try:
            if is_good_time_to_run():
                run_bot()
                
                # Random delay between runs (2-6 hours)
                next_run_delay = random.uniform(2*3600, 6*3600)
                next_run_time = datetime.now() + timedelta(seconds=next_run_delay)
                
                logging.info(f"Next bot run scheduled for: {next_run_time.strftime('%Y-%m-%d %H:%M:%S')}")
                time.sleep(next_run_delay)
            else:
                # Check again in 30-60 minutes
                check_delay = random.uniform(1800, 3600)
                logging.info(f"Not a good time to run. Checking again in {check_delay/60:.1f} minutes")
                time.sleep(check_delay)
                
        except KeyboardInterrupt:
            logging.info("Scheduler stopped by user")
            break
        except Exception as e:
            logging.error(f"Scheduler error: {e}")
            # Wait 10 minutes before retrying
            time.sleep(600)

if __name__ == "__main__":
    main()

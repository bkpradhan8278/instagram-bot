import time
import os
from datetime import datetime

def check_bot_status():
    """Simple bot status checker"""
    
    print("🤖 Instagram Bot Status Checker")
    print("=" * 40)
    
    # Check if log files exist
    if os.path.exists("scheduler.log"):
        print("✅ Scheduler log found")
        # Get last line from scheduler log
        with open("scheduler.log", "r") as f:
            lines = f.readlines()
            if lines:
                last_line = lines[-1].strip()
                print(f"📝 Last scheduler activity: {last_line}")
    else:
        print("❌ No scheduler log found")
    
    if os.path.exists("ig_bot.log"):
        print("✅ Bot log found")
        # Get last few lines from bot log
        with open("ig_bot.log", "r") as f:
            lines = f.readlines()
            if lines:
                print("📝 Recent bot activity:")
                for line in lines[-3:]:
                    print(f"   {line.strip()}")
    else:
        print("❌ No bot log found")
    
    # Check session file
    if os.path.exists("session.json"):
        print("✅ Session file exists")
    else:
        print("❌ No session file (first run)")
    
    print(f"\n🕒 Status checked at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 40)

if __name__ == "__main__":
    while True:
        try:
            check_bot_status()
            time.sleep(30)  # Check every 30 seconds
        except KeyboardInterrupt:
            print("\n👋 Status checker stopped")
            break

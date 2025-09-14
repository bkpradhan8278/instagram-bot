#!/usr/bin/env python3
"""
Instagram Bot Mode Switcher
Easy way to run the bot in different modes
"""

import subprocess
import sys
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s")

def run_visual_mode():
    """Run bot with browser display (normal mode)"""
    logging.info("🖥️ Starting Instagram Bot in VISUAL MODE (with display)")
    logging.info("📋 You can see the browser window and all actions")
    
    # Modify the main bot to run in visual mode
    os.system("python web_automation_bot.py")

def run_headless_mode():
    """Run bot without browser display (background mode)"""
    logging.info("🔇 Starting Instagram Bot in HEADLESS MODE (no display)")
    logging.info("📋 Perfect for servers, VPS, or background operation")
    logging.info("📄 Check 'headless_bot.log' for activity logs")
    
    # Run the dedicated headless script
    os.system("python headless_bot.py")

def run_headless_main_bot():
    """Run main bot in headless mode by modifying the config"""
    logging.info("🔇 Starting Main Bot in HEADLESS MODE")
    
    # Read the current bot file
    with open("web_automation_bot.py", "r") as f:
        content = f.read()
    
    # Replace HEADLESS_MODE = False with HEADLESS_MODE = True
    updated_content = content.replace("HEADLESS_MODE = False", "HEADLESS_MODE = True")
    
    # Write back temporarily
    with open("web_automation_bot_temp.py", "w") as f:
        f.write(updated_content)
    
    try:
        # Run the modified version
        os.system("python web_automation_bot_temp.py")
    finally:
        # Clean up temp file
        if os.path.exists("web_automation_bot_temp.py"):
            os.remove("web_automation_bot_temp.py")

def main():
    print("\n" + "="*60)
    print("🤖 INSTAGRAM BOT - MODE SELECTOR")
    print("="*60)
    print("Choose how to run your Instagram bot:")
    print("\n1. 🖥️  VISUAL MODE - With browser display")
    print("   - See the browser window and all actions")
    print("   - Good for monitoring and debugging")
    print("   - Requires display/desktop environment")
    
    print("\n2. 🔇 HEADLESS MODE - No browser display")
    print("   - Perfect for servers, VPS, or background")
    print("   - Uses less resources")
    print("   - Runs completely in background")
    
    print("\n3. 🔇 HEADLESS (Main Bot) - Force headless on main bot")
    print("   - Modifies main bot to run headless")
    print("   - Same features as visual mode but no display")
    
    print("\n4. ❌ Exit")
    print("="*60)
    
    while True:
        try:
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == "1":
                print("\n🖥️ Starting VISUAL MODE...")
                run_visual_mode()
                break
                
            elif choice == "2":
                print("\n🔇 Starting HEADLESS MODE...")
                run_headless_mode()
                break
                
            elif choice == "3":
                print("\n🔇 Starting HEADLESS (Main Bot)...")
                run_headless_main_bot()
                break
                
            elif choice == "4":
                print("\n👋 Goodbye!")
                sys.exit(0)
                
            else:
                print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            sys.exit(0)

if __name__ == "__main__":
    main()

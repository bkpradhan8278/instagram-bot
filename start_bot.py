#!/usr/bin/env python3
"""
Instagram Bot Launcher
=====================

This script automatically detects the environment and runs the appropriate version:
- Web Service: For Render free tier with web interface
- Background Worker: For direct bot execution

Usage:
    python start_bot.py
"""

import os
import sys
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

def main():
    # Detect environment
    port = os.environ.get('PORT')
    render_service = os.environ.get('RENDER_SERVICE_NAME')
    
    if port and render_service:
        # Running on Render as web service
        logging.info("🌐 Detected Render web service environment")
        logging.info(f"🚀 Starting web service on port {port}")
        
        try:
            from web_service_bot import app
            app.run(host='0.0.0.0', port=int(port), debug=False)
        except ImportError:
            logging.error("❌ Flask not available, falling back to direct bot")
            from web_automation_bot import main_with_restart
            main_with_restart()
            
    else:
        # Running locally or as background worker
        logging.info("🤖 Running as direct bot")
        from web_automation_bot import main_with_restart
        main_with_restart()

if __name__ == "__main__":
    main()

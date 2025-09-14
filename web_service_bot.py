"""
Instagram Web Service Bot - Render Free Tier Compatible
=====================================================

This version runs as a web service on Render's free tier.
It includes a simple web interface and keeps the service alive.

Features:
- Web interface at /
- Bot status at /status  
- Start bot at /start
- Stop bot at /stop
- Keeps service alive to prevent sleeping
"""

from flask import Flask, jsonify, render_template_string
import threading
import time
import logging
import os
from web_automation_bot import InstagramWebBot, main

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

app = Flask(__name__)

# Bot state
bot_thread = None
bot_running = False
bot_stats = {
    "status": "stopped",
    "start_time": None,
    "cycles": 0,
    "follows": 0,
    "likes": 0
}

# Simple HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Instagram Bot - 24/7 Automation</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { text-align: center; color: #333; margin-bottom: 30px; }
        .status { padding: 20px; border-radius: 5px; margin: 20px 0; text-align: center; font-weight: bold; }
        .running { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .stopped { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        .btn { padding: 12px 24px; margin: 10px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
        .btn:hover { background: #0056b3; }
        .btn:disabled { background: #6c757d; cursor: not-allowed; }
        .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }
        .stat-card { background: #e9ecef; padding: 20px; border-radius: 5px; text-align: center; }
        .stat-number { font-size: 24px; font-weight: bold; color: #007bff; }
        .logs { background: #f8f9fa; padding: 20px; border-radius: 5px; font-family: monospace; font-size: 12px; max-height: 300px; overflow-y: auto; }
        .refresh { margin: 20px 0; }
    </style>
    <script>
        function startBot() {
            fetch('/start', {method: 'POST'})
                .then(response => response.json())
                .then(data => {
                    alert(data.message);
                    location.reload();
                });
        }
        
        function stopBot() {
            fetch('/stop', {method: 'POST'})
                .then(response => response.json())
                .then(data => {
                    alert(data.message);
                    location.reload();
                });
        }
        
        function refreshStatus() {
            location.reload();
        }
        
        // Auto-refresh every 30 seconds
        setInterval(refreshStatus, 30000);
    </script>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Instagram Bot Control Panel</h1>
            <p>24/7 Automation Dashboard</p>
        </div>
        
        <div class="status {{ 'running' if status == 'running' else 'stopped' }}">
            Status: {{ status.upper() }}
            {% if start_time %}
            <br>Running since: {{ start_time }}
            {% endif %}
        </div>
        
        <div style="text-align: center; margin: 20px 0;">
            <button class="btn" onclick="startBot()" {{ 'disabled' if status == 'running' else '' }}>
                🚀 Start Bot
            </button>
            <button class="btn" onclick="stopBot()" {{ 'disabled' if status == 'stopped' else '' }}>
                🛑 Stop Bot
            </button>
            <button class="btn" onclick="refreshStatus()">
                🔄 Refresh
            </button>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{{ cycles }}</div>
                <div>Cycles Complete</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ follows }}</div>
                <div>Total Follows</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{{ likes }}</div>
                <div>Total Likes</div>
            </div>
        </div>
        
        <div class="refresh">
            <h3>🎯 Target Accounts:</h3>
            <p>lavanya.das_, shreeyasatapathy, bashu_sanchita</p>
            
            <h3>⚙️ Settings:</h3>
            <p>Conservative Mode: 200 follows/day | Headless: Yes | Session Persistence: Enabled</p>
        </div>
        
        <div class="logs">
            <h4>📋 Recent Activity:</h4>
            <p>Bot logs will appear here when running...</p>
            <p>Page auto-refreshes every 30 seconds</p>
        </div>
    </div>
</body>
</html>
"""

def run_bot():
    """Run the Instagram bot in a separate thread"""
    global bot_running, bot_stats
    
    try:
        logging.info("🤖 Starting Instagram bot thread...")
        bot_stats["status"] = "running"
        bot_stats["start_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
        
        # Check for environment variables
        username = os.environ.get("INSTAGRAM_USERNAME")
        password = os.environ.get("INSTAGRAM_PASSWORD")
        
        if not username or not password:
            logging.error("❌ Missing credentials! Please set INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD environment variables")
            bot_stats["status"] = "error"
            bot_running = False
            return
        
        # Import and run the main bot function
        main()
        
    except Exception as e:
        logging.error(f"Bot error: {e}")
    finally:
        bot_running = False
        bot_stats["status"] = "stopped"

@app.route('/')
def dashboard():
    """Main dashboard"""
    return render_template_string(HTML_TEMPLATE, **bot_stats)

@app.route('/status')
def status():
    """API endpoint for bot status"""
    return jsonify(bot_stats)

@app.route('/start', methods=['POST'])
def start_bot():
    """Start the bot"""
    global bot_thread, bot_running
    
    if bot_running:
        return jsonify({"message": "Bot is already running!", "status": "error"})
    
    try:
        bot_running = True
        bot_thread = threading.Thread(target=run_bot, daemon=True)
        bot_thread.start()
        
        return jsonify({"message": "Bot started successfully!", "status": "success"})
    except Exception as e:
        bot_running = False
        return jsonify({"message": f"Failed to start bot: {e}", "status": "error"})

@app.route('/stop', methods=['POST'])
def stop_bot():
    """Stop the bot"""
    global bot_running
    
    if not bot_running:
        return jsonify({"message": "Bot is not running!", "status": "error"})
    
    bot_running = False
    bot_stats["status"] = "stopping"
    
    return jsonify({"message": "Bot stop signal sent!", "status": "success"})

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": time.time(),
        "bot_running": bot_running
    })

# Keep-alive function to prevent Render free tier from sleeping
def keep_alive():
    """Send periodic requests to keep the service alive"""
    import requests
    import os
    
    while True:
        try:
            # Get the service URL from environment or use localhost
            service_url = os.environ.get('RENDER_EXTERNAL_URL', 'http://localhost:5000')
            requests.get(f"{service_url}/health", timeout=10)
            logging.info("🔄 Keep-alive ping sent")
        except Exception as e:
            logging.warning(f"Keep-alive failed: {e}")
        
        # Wait 10 minutes before next ping
        time.sleep(600)

if __name__ == '__main__':
    # Start keep-alive thread
    keep_alive_thread = threading.Thread(target=keep_alive, daemon=True)
    keep_alive_thread.start()
    
    # Get port from environment (Render sets this)
    port = int(os.environ.get('PORT', 5000))
    
    logging.info(f"🚀 Starting web service on port {port}")
    logging.info("🌐 Dashboard will be available at your Render URL")
    
    # Run Flask app
    app.run(host='0.0.0.0', port=port, debug=False)

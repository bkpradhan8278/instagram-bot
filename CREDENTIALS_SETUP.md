# 🔐 Instagram Bot - Secure Credentials Setup Guide

## 🎯 Overview
Your Instagram credentials are now secure! They're no longer hardcoded in the bot files.

## 🛡️ Security Benefits
- ✅ **No passwords in code** - Safe to share and deploy
- ✅ **Environment variables** - Industry standard security
- ✅ **Git-safe** - Credentials never committed to repository
- ✅ **Platform flexible** - Works locally and on cloud

---

## 📋 How to Set Your Credentials

### **Method 1: For Local Development (Windows)**

**Option A: PowerShell (Recommended)**
```powershell
# Set environment variables in PowerShell
$env:INSTAGRAM_USERNAME = "bi.pali8278@gmail.com"
$env:INSTAGRAM_PASSWORD = "Bk8278@@"

# Run the bot
python web_automation_bot.py
```

**Option B: Command Prompt**
```cmd
# Set environment variables in CMD
set INSTAGRAM_USERNAME=bi.pali8278@gmail.com
set INSTAGRAM_PASSWORD=Bk8278@@

# Run the bot
python web_automation_bot.py
```

**Option C: Create .env file (Easy)**
1. Copy `.env.example` to `.env`
2. Edit `.env` file:
```env
INSTAGRAM_USERNAME=bi.pali8278@gmail.com
INSTAGRAM_PASSWORD=Bk8278@@
```
3. Install python-dotenv: `pip install python-dotenv`
4. The bot will automatically load from .env file

---

### **Method 2: For Render Deployment**

When deploying to Render:

1. **Go to your Render service dashboard**
2. **Click "Environment"** 
3. **Add environment variables:**
   - **Key:** `INSTAGRAM_USERNAME`
   - **Value:** `bi.pali8278@gmail.com`
   - **Key:** `INSTAGRAM_PASSWORD` 
   - **Value:** `Bk8278@@`
4. **Click "Save"**
5. **Deploy!**

---

### **Method 3: For Other Cloud Platforms**

**Heroku:**
```bash
heroku config:set INSTAGRAM_USERNAME="bi.pali8278@gmail.com"
heroku config:set INSTAGRAM_PASSWORD="Bk8278@@"
```

**Railway:**
- Go to Variables tab
- Add INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD

**AWS/Docker:**
```bash
docker run -e INSTAGRAM_USERNAME="bi.pali8278@gmail.com" -e INSTAGRAM_PASSWORD="Bk8278@@" your-bot
```

---

## 🔍 Verification

The bot will show this message if credentials are missing:
```
❌ Missing credentials! Please set INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD environment variables
💡 Example: export INSTAGRAM_USERNAME='your_email@gmail.com'
💡 Example: export INSTAGRAM_PASSWORD='your_password'
```

---

## 🚨 Important Security Notes

1. **Never commit .env files** - They're in .gitignore
2. **Keep credentials private** - Don't share in screenshots/logs
3. **Use app passwords** - Consider Instagram app-specific passwords
4. **Rotate regularly** - Change passwords periodically

---

## 🎯 Quick Start Commands

**PowerShell (Windows):**
```powershell
$env:INSTAGRAM_USERNAME = "bi.pali8278@gmail.com"
$env:INSTAGRAM_PASSWORD = "Bk8278@@"
python web_automation_bot.py
```

**Web Service:**
```powershell
$env:INSTAGRAM_USERNAME = "bi.pali8278@gmail.com"
$env:INSTAGRAM_PASSWORD = "Bk8278@@"
python web_service_bot.py
```

Your bot is now secure and ready for deployment! 🚀

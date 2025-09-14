#!/usr/bin/env python3
"""
Simple login test to check if Instagram account is accessible
"""
import time
from instagrapi import Client

USERNAME = "niveshwithrishabh"
PASSWORD = "Asdfghjkl@12"

def test_login():
    print("🧪 Testing Instagram login...")
    
    cl = Client()
    cl.delay_range = [1, 3]
    
    try:
        # Try fresh login
        print("📡 Attempting login...")
        cl.login(USERNAME, PASSWORD)
        print("✅ Login successful!")
        
        # Test basic API call
        print("🔍 Testing basic account info...")
        user_info = cl.account_info()
        print(f"✅ Account info retrieved: @{user_info.username}")
        print(f"📊 Account ID: {user_info.pk}")
        
        # Test another API call
        print("🔍 Testing user lookup...")
        my_full_info = cl.user_info(user_info.pk)
        print(f"✅ Full user info retrieved")
        print(f"📊 Followers: {my_full_info.follower_count}")
        print(f"📊 Following: {my_full_info.following_count}")
        
        # Test logout
        cl.logout()
        print("✅ Logout successful!")
        
        return True
        
    except Exception as e:
        print(f"❌ Login failed: {e}")
        return False

if __name__ == "__main__":
    test_login()

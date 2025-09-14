import time
from datetime import datetime
from instagrapi import Client

USERNAME = "niveshwithrishabh"
PASSWORD = "Asdfghjkl@12"

def test_account_status():
    print(f"Testing account at {datetime.now()}")
    
    cl = Client()
    cl.delay_range = [2, 5]  # Slower requests
    
    try:
        # Simple login test
        cl.login(USERNAME, PASSWORD)
        print("✅ Login successful")
        
        # Get own profile (safest API call)
        my_info = cl.account_info()
        print(f"✅ Account info: @{my_info.username}")
        print(f"   Followers: {my_info.follower_count}")
        print(f"   Following: {my_info.following_count}")
        
        cl.logout()
        print("✅ Test completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    test_account_status()

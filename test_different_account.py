import time
from datetime import datetime
from instagrapi import Client

def test_different_account(username, password):
    print(f"Testing account: {username} at {datetime.now()}")
    
    cl = Client()
    cl.delay_range = [2, 5]  # Slower requests
    
    try:
        # Simple login test
        cl.login(username, password)
        print("✅ Login successful")
        
        # Get own profile (safest API call)
        my_info = cl.account_info()
        print(f"✅ Account info: @{my_info.username}")
        
        # Try to get follower/following counts (might not be available for all accounts)
        try:
            user_info = cl.user_info(cl.user_id)
            print(f"   Followers: {user_info.follower_count}")
            print(f"   Following: {user_info.following_count}")
        except Exception as e:
            print(f"   Note: Could not get follower counts: {e}")
            print("   This is normal for some accounts and doesn't affect the bot")
        
        # Test fetching a popular public account (less likely to be restricted)
        try:
            test_user = cl.user_info_by_username("instagram")  # Instagram's official account
            print(f"✅ Can fetch public accounts: @{test_user.username}")
        except Exception as e:
            print(f"❌ Cannot fetch public accounts: {e}")
        
        cl.logout()
        print("✅ Test completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

# Test with different account
if __name__ == "__main__":
    current_username = "bi.pali8278@gmail.com"
    current_password = "Bk8278@@"
    
    print("=" * 50)
    print("TESTING CURRENT ACCOUNT")
    print("=" * 50)
    result = test_different_account(current_username, current_password)
    
    if not result:
        print("\n" + "=" * 50)
        print("CURRENT ACCOUNT HAS ISSUES")
        print("=" * 50)
        print("Options:")
        print("1. Wait 24-48 hours for rate limit to reset")
        print("2. Create a new Instagram account")
        print("3. Use a different existing account")
        print("\nTo test a different account, edit this file and change the credentials.")
    else:
        print("\n✅ Account is working! The issue might be with specific API calls.")

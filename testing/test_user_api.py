import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
import json

User = get_user_model()

def test_user_api():
    print("🔧 TESTING USER MANAGEMENT API")
    print("=" * 50)
    
    client = APIClient()
    
    # Get a superuser
    superuser = User.objects.filter(is_superuser=True).first()
    if not superuser:
        print("No superuser found!")
        return
    
    # Force authenticate
    client.force_authenticate(user=superuser)
    
    print(f"Testing with user: {superuser.email}")
    
    # Test the user list endpoint
    print("\n📋 Testing user list endpoint...")
    response = client.get('/api/accounts/admin/users/')
    
    print(f"Status Code: {response.status_code}")
    print(f"Response Content-Type: {response.get('Content-Type', 'Unknown')}")
    
    if response.status_code == 200:
        print(f"✅ Success! Response type: {type(response.data)}")
        print(f"Response data: {response.data}")
        
        # Check if it's a list or something else
        if isinstance(response.data, list):
            print(f"Found {len(response.data)} users")
            for i, user in enumerate(response.data):
                print(f"  {i+1}. Type: {type(user)}, Value: {user}")
        else:
            print(f"Response is not a list. Type: {type(response.data)}")
            print("Full response:", json.dumps(response.data, indent=2))
    else:
        print(f"❌ Failed: {response.status_code}")
        print(f"Response: {response.data}")
    
    return response

if __name__ == "__main__":
    test_user_api()
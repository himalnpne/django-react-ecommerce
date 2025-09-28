import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
import json

User = get_user_model()

def test_products_api():
    print("🔧 TESTING PRODUCTS API ENDPOINT")
    print("=" * 50)
    
    client = Client()
    
    # First, login to get token
    login_data = {
        'email': 'admin@example.com',
        'password': 'admin123'
    }
    
    print("🔑 Logging in...")
    login_response = client.post(
        '/api/accounts/login/',
        data=json.dumps(login_data),
        content_type='application/json'
    )
    
    if login_response.status_code != 200:
        print("❌ Login failed")
        return
    
    login_data = login_response.json()
    token = login_data.get('access')
    
    if not token:
        print("❌ No token received")
        return
    
    print("✅ Login successful")
    
    # Test the products admin endpoint
    print("\n📦 Testing products admin endpoint...")
    
    # Add Authorization header
    headers = {
        'HTTP_AUTHORIZATION': f'Bearer {token}',
        'content_type': 'application/json'
    }
    
    response = client.get('/api/products/admin/products/', **headers)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response Content-Type: {response.get('Content-Type')}")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Products API Response:")
        print(f"Response type: {type(data)}")
        print(f"Is array: {isinstance(data, list)}")
        
        if isinstance(data, list):
            print(f"Found {len(data)} products in array")
            for i, product in enumerate(data[:3]):  # Show first 3 products
                print(f"  {i+1}. {product.get('name', 'No name')} (ID: {product.get('id')})")
        elif isinstance(data, dict):
            print("Response is an object/dictionary")
            print("Keys:", list(data.keys()))
            if 'results' in data and isinstance(data['results'], list):
                print(f"Found {len(data['results'])} products in 'results' array")
                for i, product in enumerate(data['results'][:3]):
                    print(f"  {i+1}. {product.get('name', 'No name')} (ID: {product.get('id')})")
            else:
                print("Full response structure:")
                print(json.dumps(data, indent=2))
        else:
            print(f"Unexpected response type: {type(data)}")
    else:
        print(f"❌ Products API failed: {response.status_code}")
        print(f"Error: {response.json()}")

if __name__ == "__main__":
    test_products_api()
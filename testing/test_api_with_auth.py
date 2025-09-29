import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from orders.views import admin_dashboard_stats

User = get_user_model()

def test_api_with_auth():
    print("🔧 TESTING API ENDPOINT WITH AUTHENTICATION")
    print("=" * 50)
    
    # Use Django test client which handles authentication
    client = APIClient()
    
    # Get or create a superuser
    superuser = User.objects.filter(is_superuser=True).first()
    if not superuser:
        print("No superuser found, creating one...")
        superuser = User.objects.create_superuser(
            email='test@admin.com',
            username='testadmin',
            password='testpass123'
        )
    
    # Force authenticate
    client.force_authenticate(user=superuser)
    
    print(f"Testing with user: {superuser.email}")
    print(f"User is staff: {superuser.is_staff}")
    print(f"User is superuser: {superuser.is_superuser}")
    
    # Make the API request
    response = client.get('/api/orders/admin-dashboard-stats/')
    
    print(f"\n📊 API RESPONSE:")
    print(f"Status Code: {response.status_code}")
    print(f"Data: {response.data}")
    
    return response

if __name__ == "__main__":
    test_api_with_auth()
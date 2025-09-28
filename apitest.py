import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth import get_user_model
from orders.views import admin_dashboard_stats

User = get_user_model()

def test_api_endpoint():
    print("🔧 TESTING API ENDPOINT")
    print("=" * 50)
    
    # Create a test request
    factory = RequestFactory()
    
    # Create a superuser for testing
    try:
        superuser = User.objects.filter(is_superuser=True).first()
        if not superuser:
            # Create a test superuser if none exists
            superuser = User.objects.create_superuser(
                email='test@admin.com',
                username='testadmin',
                password='testpass123'
            )
            print("Created test superuser")
    except Exception as e:
        print(f"Error creating test user: {e}")
        return
    
    # Create request
    request = factory.get('/api/orders/admin-dashboard-stats/')
    request.user = superuser
    
    print(f"Testing with user: {superuser.email}")
    print(f"User is staff: {superuser.is_staff}")
    print(f"User is superuser: {superuser.is_superuser}")
    
    # Call the view function
    try:
        response = admin_dashboard_stats(request)
        print(f"\n📊 API RESPONSE:")
        print(f"Status Code: {response.status_code}")
        print(f"Data: {response.data}")
    except Exception as e:
        print(f"❌ API Error: {e}")

if __name__ == "__main__":
    test_api_endpoint()
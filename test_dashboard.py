import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.db.models import Sum
from decimal import Decimal

# Try to import models with error handling
try:
    from products.models import Product
    PRODUCTS_AVAILABLE = True
except ImportError as e:
    print(f"Products model not available: {e}")
    PRODUCTS_AVAILABLE = False

try:
    from orders.models import Order
    ORDERS_AVAILABLE = True
except ImportError as e:
    print(f"Orders model not available: {e}")
    ORDERS_AVAILABLE = False

User = get_user_model()

def test_dashboard_data():
    print("🔍 TESTING DASHBOARD DATA")
    print("=" * 50)
    
    # Test Users
    print("\n👥 USERS:")
    total_users = User.objects.count()
    print(f"Total Users: {total_users}")
    
    if total_users > 0:
        users = User.objects.all()[:3]
        for i, user in enumerate(users):
            print(f"  {i+1}. {user.email} (ID: {user.id})")
            print(f"     Staff: {user.is_staff}, Superuser: {user.is_superuser}")
    else:
        print("  No users found in database!")
    
    # Test Products
    print("\n📦 PRODUCTS:")
    if PRODUCTS_AVAILABLE:
        total_products = Product.objects.count()
        print(f"Total Products: {total_products}")
        
        if total_products > 0:
            products = Product.objects.all()[:3]
            for i, product in enumerate(products):
                print(f"  {i+1}. {product.name} (${product.price})")
                print(f"     Category: {getattr(product.category, 'name', 'None')}")
        else:
            print("  No products found in database!")
    else:
        print("  Products model not available")
    
    # Test Orders
    print("\n🛒 ORDERS:")
    if ORDERS_AVAILABLE:
        total_orders = Order.objects.count()
        print(f"Total Orders: {total_orders}")
        
        if total_orders > 0:
            orders = Order.objects.all()[:3]
            for i, order in enumerate(orders):
                print(f"  {i+1}. Order #{order.id}")
                print(f"     User: {order.user.email}")
                print(f"     Product: {order.product.name}")
                print(f"     Total: ${order.total_price}")
                print(f"     Status: {order.status}")
            
            # Calculate revenue
            revenue_result = Order.objects.aggregate(total=Sum('total_price'))
            total_revenue = revenue_result.get('total', 0) or 0
            if isinstance(total_revenue, Decimal):
                total_revenue = float(total_revenue)
            print(f"Total Revenue: ${total_revenue}")
        else:
            print("  No orders found in database!")
    else:
        print("  Orders model not available")
    
    print("\n" + "=" * 50)
    print("Expected API Response Structure:")
    expected_response = {
        "totalUsers": total_users,
        "totalProducts": total_products if PRODUCTS_AVAILABLE else 0,
        "totalOrders": total_orders if ORDERS_AVAILABLE else 0,
        "totalRevenue": total_revenue if ORDERS_AVAILABLE else 0,
    }
    print(expected_response)

if __name__ == "__main__":
    test_dashboard_data()
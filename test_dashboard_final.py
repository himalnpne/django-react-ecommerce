import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.db.models import Sum
from decimal import Decimal

User = get_user_model()

def test_all_data():
    print("🔍 COMPREHENSIVE DASHBOARD TEST")
    print("=" * 60)
    
    # Test Users
    print("\n👥 USERS DATA:")
    total_users = User.objects.count()
    print(f"Total Users: {total_users}")
    
    users = User.objects.all()
    for user in users:
        print(f"  - {user.email} (ID: {user.id}, Staff: {user.is_staff}, Superuser: {user.is_superuser})")
    
    # Test Products
    print("\n📦 PRODUCTS DATA:")
    try:
        from products.models import Product, Category
        total_products = Product.objects.count()
        print(f"Total Products: {total_products}")
        
        products = Product.objects.all()
        for product in products:
            print(f"  - {product.name} (${product.price}, Stock: {product.stock_quantity}, Active: {product.is_active})")
    except Exception as e:
        print(f"  Error with products: {e}")
        total_products = 0
    
    # Test Orders
    print("\n🛒 ORDERS DATA:")
    try:
        from orders.models import Order
        total_orders = Order.objects.count()
        print(f"Total Orders: {total_orders}")
        
        if total_orders > 0:
            orders = Order.objects.all()
            for order in orders:
                print(f"  - Order #{order.id}: {order.user.email} -> {order.product.name} (Qty: {order.quantity}, Total: ${order.total_price}, Status: {order.status})")
            
            # Calculate revenue
            revenue_result = Order.objects.aggregate(total=Sum('total_price'))
            total_revenue = revenue_result.get('total', 0) or 0
            if isinstance(total_revenue, Decimal):
                total_revenue = float(total_revenue)
            print(f"Total Revenue: ${total_revenue}")
        else:
            print("  No orders in database")
            total_revenue = 0
    except Exception as e:
        print(f"  Error with orders: {e}")
        total_orders = 0
        total_revenue = 0
    
    print("\n📊 EXPECTED DASHBOARD DATA:")
    expected_data = {
        "totalUsers": total_users,
        "totalProducts": total_products,
        "totalOrders": total_orders,
        "totalRevenue": total_revenue,
    }
    print(expected_data)
    
    print("\n🔧 DEBUGGING STEPS:")
    print("1. Check browser console for API response")
    print("2. Check Network tab for the admin-dashboard-stats request")
    print("3. Verify the API returns the above data")
    print("4. Check if there are any JavaScript errors")
    
    return expected_data

if __name__ == "__main__":
    test_all_data()
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')
django.setup()

from products.models import Category, Product
from accounts.models import CustomUser

def create_sample_data():
    print("Creating sample data...")
    
    # Create admin user if not exists
    if not CustomUser.objects.filter(email='admin@example.com').exists():
        admin_user = CustomUser.objects.create_superuser(
            email='admin@test.com',
            username='testadmin',
            password='testadminpassword',
            first_name='Admin',
            last_name='User'
        )
        print("Created admin user: admin@example.com / admin123")
    
    # Create categories
    categories_data = [
        {"name": "Electronics", "description": "Latest electronic devices"},
        {"name": "Clothing", "description": "Fashionable clothing items"},
        {"name": "Books", "description": "Various books and literature"},
    ]
    
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data["name"],
            defaults={"description": cat_data["description"]}
        )
        if created:
            print(f"Created category: {category.name}")
    
    # Create sample products
    electronics = Category.objects.get(name="Electronics")
    clothing = Category.objects.get(name="Clothing")
    
    products_data = [
        {
            "name": "iPhone 14 Pro", 
            "price": 999.99, 
            "category": electronics, 
            "stock_quantity": 50,
            "description": "Latest iPhone with advanced features"
        },
        {
            "name": "MacBook Pro", 
            "price": 1999.99, 
            "category": electronics, 
            "stock_quantity": 30,
            "description": "Powerful laptop for professionals"
        },
        {
            "name": "Cotton T-Shirt", 
            "price": 24.99, 
            "category": clothing, 
            "stock_quantity": 200,
            "description": "Comfortable cotton t-shirt"
        },
    ]
    
    for product_data in products_data:
        product, created = Product.objects.get_or_create(
            name=product_data["name"],
            defaults={
                "description": product_data["description"],
                "price": product_data["price"],
                "category": product_data["category"],
                "stock_quantity": product_data["stock_quantity"],
                "is_active": True
            }
        )
        if created:
            print(f"Created product: {product.name} - ${product.price}")

if __name__ == "__main__":
    create_sample_data()
    print("Sample data creation completed!")
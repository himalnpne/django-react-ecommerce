import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')
django.setup()

from django.core.management import execute_from_command_line
from django.db import connection

def check_migrations():
    print("🔍 CHECKING MIGRATION STATUS")
    print("=" * 50)
    
    # Check if orders_order table exists
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_name = 'orders_order'
        """)
        table_exists = cursor.fetchone()
        
        if table_exists:
            print("✅ orders_order table exists")
        else:
            print("❌ orders_order table does NOT exist")
            print("Run these commands:")
            print("  python manage.py makemigrations orders")
            print("  python manage.py migrate")
    
    # Check for pending migrations
    print("\n📋 Checking for pending migrations...")
    os.system("python manage.py showmigrations")

if __name__ == "__main__":
    check_migrations()
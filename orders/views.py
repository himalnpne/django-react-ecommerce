from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status, generics
from django.db.models import Sum
from decimal import Decimal
import logging

# Import models with error handling
try:
    from products.models import Product
except ImportError as e:
    print(f"Error importing Product model: {e}")
    Product = None

try:
    from orders.models import Order
except ImportError as e:
    print(f"Error importing Order model: {e}")
    Order = None

logger = logging.getLogger(__name__)
User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin_dashboard_stats(request):
    try:
        print(f"Dashboard stats requested by user: {request.user}")
        print(f"User is authenticated: {request.user.is_authenticated}")
        print(f"User is staff: {request.user.is_staff}")
        print(f"User is superuser: {request.user.is_superuser}")
        
        # Check if user has admin privileges (optional - remove if you want all authenticated users to access)
        if not (request.user.is_staff or request.user.is_superuser):
            return Response(
                {"detail": "Admin privileges required."}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get total users count
        try:
            total_users = User.objects.count()
            print(f"Total users: {total_users}")
        except Exception as e:
            print(f"Error counting users: {e}")
            total_users = 0
        
        # Get total products count
        try:
            if Product:
                total_products = Product.objects.count()
            else:
                total_products = 0
            print(f"Total products: {total_products}")
        except Exception as e:
            print(f"Error counting products: {e}")
            total_products = 0
        
        # Get total orders count
        try:
            if Order:
                total_orders = Order.objects.count()
            else:
                total_orders = 0
            print(f"Total orders: {total_orders}")
        except Exception as e:
            print(f"Error counting orders: {e}")
            total_orders = 0
        
        # Get total revenue
        try:
            if Order and total_orders > 0:
                revenue_aggregate = Order.objects.aggregate(total=Sum('total_price'))
                total_revenue = revenue_aggregate.get('total', 0) or 0
                # Convert Decimal to float for JSON serialization
                if isinstance(total_revenue, Decimal):
                    total_revenue = float(total_revenue)
            else:
                total_revenue = 0
            print(f"Total revenue: {total_revenue}")
        except Exception as e:
            print(f"Error calculating revenue: {e}")
            total_revenue = 0

        response_data = {
            "totalUsers": total_users,
            "totalProducts": total_products,
            "totalOrders": total_orders,
            "totalRevenue": total_revenue,
        }
        
        print(f"Sending response data: {response_data}")
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        error_message = f"Error in admin_dashboard_stats: {str(e)}"
        logger.error(error_message)
        print(error_message)
        
        return Response(
            {
                "error": "Failed to fetch dashboard statistics",
                "detail": str(e) if hasattr(e, '__str__') else "Unknown error"
            }, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class OrderListView(generics.ListAPIView):
    """Admin endpoint to list all orders"""
    permission_classes = [IsAdminUser]
    
    def get_queryset(self):
        return Order.objects.all().select_related('user', 'product')
    
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            
            # Simple serializer for order data
            orders_data = []
            for order in queryset:
                orders_data.append({
                    'id': order.id,
                    'user': {
                        'id': order.user.id,
                        'email': order.user.email,
                        'username': order.user.username
                    },
                    'product': {
                        'id': order.product.id,
                        'name': order.product.name,
                        'price': str(order.product.price)
                    },
                    'quantity': order.quantity,
                    'total_price': str(order.total_price),
                    'status': order.status,
                    'created_at': order.created_at
                })
            
            return Response(orders_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {"error": f"Failed to fetch orders: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
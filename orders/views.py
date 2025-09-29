from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import Order, OrderItem
from cart.models import Cart, CartItem
from products.models import Product
from rest_framework.views import APIView
from rest_framework.response import Response

@api_view(['POST'])
@permission_classes([AllowAny])
def create_order(request):
    try:
        with transaction.atomic():
            # Get cart items based on user authentication
            cart_items = []
            if request.user.is_authenticated:
                cart = get_object_or_404(Cart, user=request.user)
                cart_items = cart.items.all()
            
            if not cart_items and not request.data.get('cart_items'):
                return Response({'error': 'No items in cart'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Validate required fields
            required_fields = ['guest_phone', 'address', 'city', 'state', 'zip_code']
            for field in required_fields:
                if not request.data.get(field):
                    return Response({'error': f'{field} is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Calculate total amount
            total_amount = 0
            order_items_data = []
            
            if request.user.is_authenticated:
                for cart_item in cart_items:
                    product = cart_item.product
                    if product.stock_quantity < cart_item.quantity:
                        return Response(
                            {'error': f'Not enough stock for {product.name}'}, 
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    
                    item_total = cart_item.quantity * product.price
                    total_amount += item_total
                    
                    order_items_data.append({
                        'product': product,
                        'quantity': cart_item.quantity,
                        'price': product.price
                    })
            else:
                # For guest users, validate products from request data
                for item_data in request.data.get('cart_items', []):
                    product = get_object_or_404(Product, id=item_data['product_id'])
                    quantity = item_data['quantity']
                    
                    if product.stock_quantity < quantity:
                        return Response(
                            {'error': f'Not enough stock for {product.name}'}, 
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    
                    item_total = quantity * product.price
                    total_amount += item_total
                    
                    order_items_data.append({
                        'product': product,
                        'quantity': quantity,
                        'price': product.price
                    })
            
            # Create order
            order_data = {
                'total_price': total_amount,
                'guest_phone': request.data.get('guest_phone'),
                'address': request.data.get('address'),
                'city': request.data.get('city'),
                'state': request.data.get('state'),
                'country': request.data.get('country', 'United States'),
                'zip_code': request.data.get('zip_code'),
            }
            
            # Add location coordinates if provided
            if request.data.get('latitude') and request.data.get('longitude'):
                order_data['latitude'] = request.data.get('latitude')
                order_data['longitude'] = request.data.get('longitude')
            
            # Add user info for authenticated users
            if request.user.is_authenticated:
                order_data['user'] = request.user
            else:
                # Add guest info if provided
                if request.data.get('guest_email'):
                    order_data['guest_email'] = request.data.get('guest_email')
                if request.data.get('guest_name'):
                    order_data['guest_name'] = request.data.get('guest_name')
            
            order = Order.objects.create(**order_data)
            
            # Create order items
            for item_data in order_items_data:
                OrderItem.objects.create(
                    order=order,
                    product=item_data['product'],
                    quantity=item_data['quantity'],
                    price=item_data['price']
                )
                
                # Update product stock
                item_data['product'].stock_quantity -= item_data['quantity']
                item_data['product'].save()
            
            # Clear cart for authenticated users
            if request.user.is_authenticated:
                cart.items.all().delete()
            
            return Response({
                'success': 'Order created successfully',
                'order_id': order.id,
                'total_amount': str(total_amount)
            }, status=status.HTTP_201_CREATED)
            
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    orders_data = []
    for order in orders:
        orders_data.append({
            'id': order.id,
            'total_price': str(order.total_price),
            'status': order.status,
            'payment_status': order.payment_status,
            'created_at': order.created_at,
            'items_count': order.items.count()
        })
    
    return Response({'orders': orders_data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    items_data = []
    for item in order.items.all():
        items_data.append({
            'product': {
                'id': item.product.id,
                'name': item.product.name,
                'image_url': item.product.image_url,
            },
            'quantity': item.quantity,
            'price': str(item.price),
            'total_price': str(item.total_price)
        })
    
    order_data = {
        'id': order.id,
        'total_price': str(order.total_price),
        'status': order.status,
        'payment_status': order.payment_status,
        'created_at': order.created_at,
        'address': order.address,
        'city': order.city,
        'state': order.state,
        'country': order.country,
        'zip_code': order.zip_code,
        'guest_phone': order.guest_phone,
        'items': items_data
    }
    
    return Response(order_data)

# Keep your existing admin views if they exist
def admin_dashboard_stats(request):
    # Your existing admin dashboard stats function
    from django.http import JsonResponse
    return JsonResponse({'message': 'Admin stats endpoint'})

class OrderListView(APIView):
    def get(self, request):
        # Your existing admin order list view
        return Response({'message': 'Admin orders endpoint'})
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from products.models import Product

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = []
    
    for item in cart.items.all():
        items.append({
            'id': item.id,
            'product': {
                'id': item.product.id,
                'name': item.product.name,
                'price': str(item.product.price),
                'image_url': item.product.image_url,
            },
            'quantity': item.quantity,
            'total_price': str(item.total_price)
        })
    
    return Response({
        'items': items,
        'total_price': str(cart.total_price),
        'total_items': cart.total_items
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    product_id = request.data.get('product_id')
    quantity = int(request.data.get('quantity', 1))
    
    if not product_id:
        return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    product = get_object_or_404(Product, id=product_id)
    
    if product.stock_quantity < quantity:
        return Response({'error': 'Not enough stock available'}, status=status.HTTP_400_BAD_REQUEST)
    
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Check if item already exists in cart
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not created:
        # Update quantity if item already exists
        cart_item.quantity += quantity
        cart_item.save()
    
    return Response({'success': 'Item added to cart'}, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_cart_item(request, item_id):
    quantity = request.data.get('quantity')
    
    if quantity is None:
        return Response({'error': 'Quantity is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        quantity = int(quantity)
        if quantity < 0:
            return Response({'error': 'Quantity must be positive'}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response({'error': 'Quantity must be a number'}, status=status.HTTP_400_BAD_REQUEST)
    
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    if quantity == 0:
        cart_item.delete()
        return Response({'success': 'Item removed from cart'})
    
    # Check stock availability
    if cart_item.product.stock_quantity < quantity:
        return Response({'error': 'Not enough stock available'}, status=status.HTTP_400_BAD_REQUEST)
    
    cart_item.quantity = quantity
    cart_item.save()
    
    return Response({'success': 'Cart updated'})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    
    return Response({'success': 'Item removed from cart'})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def clear_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart.items.all().delete()
    
    return Response({'success': 'Cart cleared'})
# products/views.py
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Count, Avg, Q
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

# Admin Category Views (require admin authentication)
class CategoryListCreateView(generics.ListCreateAPIView):
    """Admin endpoint to list all categories or create new category"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Admin endpoint to get, update, or delete a specific category"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'slug'

# Admin Product Views (require admin authentication)
class ProductListCreateView(generics.ListCreateAPIView):
    """Admin endpoint to list all products or create new product"""
    queryset = Product.objects.all().select_related('category')
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Admin endpoint to get, update, or delete a specific product"""
    queryset = Product.objects.all().select_related('category')
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'slug'

# Public Category View (no authentication required)
class PublicCategoryListView(generics.ListAPIView):
    """Public endpoint to list all categories"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

# Public Views (no authentication required)
class PublicProductListView(generics.ListAPIView):
    """Public endpoint to list all active products"""
    queryset = Product.objects.filter(is_active=True).select_related('category')
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__slug=category)
        return queryset

class PublicProductDetailView(generics.RetrieveAPIView):
    """Public endpoint to get a specific product by slug"""
    queryset = Product.objects.filter(is_active=True).select_related('category')
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

# Function-based views
@api_view(['POST'])
@permission_classes([IsAdminUser])
def bulk_create_products(request):
    """Admin endpoint to bulk create products"""
    try:
        products_data = request.data.get('products', [])
        if not products_data:
            return Response(
                {"error": "No products data provided"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        created_products = []
        errors = []
        
        for product_data in products_data:
            serializer = ProductSerializer(data=product_data)
            if serializer.is_valid():
                serializer.save()
                created_products.append(serializer.data)
            else:
                errors.append({
                    'product_data': product_data,
                    'errors': serializer.errors
                })
        
        return Response({
            'created_products': created_products,
            'errors': errors,
            'created_count': len(created_products),
            'error_count': len(errors)
        }, status=status.HTTP_201_CREATED if created_products else status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        return Response(
            {"error": f"Failed to bulk create products: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([AllowAny])
def product_stats(request):
    """Public endpoint to get product statistics"""
    try:
        total_products = Product.objects.filter(is_active=True).count()
        total_categories = Category.objects.count()
        
        # Average price
        avg_price = Product.objects.filter(is_active=True).aggregate(
            avg_price=Avg('price')
        )['avg_price'] or 0
        
        # Products per category
        category_stats = Category.objects.annotate(
            product_count=Count('products', filter=Q(products__is_active=True))
        ).values('name', 'product_count')
        
        return Response({
            'total_products': total_products,
            'total_categories': total_categories,
            'average_price': round(float(avg_price), 2),
            'categories': list(category_stats)
        })
        
    except Exception as e:
        return Response(
            {"error": f"Failed to get product stats: {str(e)}"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
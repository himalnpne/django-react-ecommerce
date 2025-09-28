from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer, ProductListSerializer

# Category Views
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'

# Product Views
class ProductListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at', 'name']

    def get_queryset(self):
        return Product.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

# Public API Views (for frontend)
class PublicProductListView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']

    def get_queryset(self):
        return Product.objects.filter(is_active=True)

class PublicProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

# Bulk operations
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bulk_create_products(request):
    products_data = request.data
    created_products = []
    errors = []

    for product_data in products_data:
        serializer = ProductSerializer(data=product_data)
        if serializer.is_valid():
            product = serializer.save()
            created_products.append(ProductListSerializer(product).data)
        else:
            errors.append({
                'data': product_data,
                'errors': serializer.errors
            })

    return Response({
        'created': len(created_products),
        'products': created_products,
        'errors': errors
    }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def product_stats(request):
    total_products = Product.objects.count()
    active_products = Product.objects.filter(is_active=True).count()
    total_value = sum(product.price * product.stock_quantity for product in Product.objects.all())
    
    return Response({
        'total_products': total_products,
        'active_products': active_products,
        'total_inventory_value': round(total_value, 2)
    })
from django.urls import path
from .views import (
    CategoryListCreateView, CategoryDetailView,
    ProductListCreateView, ProductDetailView,
    PublicProductListView, PublicProductDetailView,
    bulk_create_products, product_stats
)

urlpatterns = [
    # Admin CRUD endpoints (require authentication)
    path('admin/categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('admin/categories/<slug:slug>/', CategoryDetailView.as_view(), name='category-detail'),
    path('admin/products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('admin/products/<slug:slug>/', ProductDetailView.as_view(), name='product-detail'),
    path('admin/products/bulk-create/', bulk_create_products, name='bulk-create-products'),
    
    # Public endpoints (no authentication required)
    path('public/', PublicProductListView.as_view(), name='public-products'),
    path('public/<slug:slug>/', PublicProductDetailView.as_view(), name='public-product-detail'),
    path('stats/', product_stats, name='product-stats'),
]
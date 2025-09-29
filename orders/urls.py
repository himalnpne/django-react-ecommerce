from django.urls import path
from . import views

urlpatterns = [
    # Checkout and order management endpoints
    path('create/', views.create_order, name='create_order'),
    path('', views.get_orders, name='get_orders'),
    path('<int:order_id>/', views.get_order_detail, name='order_detail'),
    
    # Admin endpoints (keep these if you need them)
    path('admin-dashboard-stats/', views.admin_dashboard_stats, name='admin-dashboard-stats'),
    path('admin/orders/', views.OrderListView.as_view(), name='admin-order-list'),
]
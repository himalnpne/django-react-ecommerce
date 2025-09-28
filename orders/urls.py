from django.urls import path
from .views import admin_dashboard_stats, OrderListView

urlpatterns = [
    path('admin-dashboard-stats/', admin_dashboard_stats, name='admin-dashboard-stats'),
    path('admin/orders/', OrderListView.as_view(), name='admin-order-list'),
]
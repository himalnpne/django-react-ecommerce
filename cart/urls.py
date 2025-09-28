from django.urls import path
from . import views

urlpatterns = [
    # Example route
    path('', views.cart_home, name='cart_home'),
]

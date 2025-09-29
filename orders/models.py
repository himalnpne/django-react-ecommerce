from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product

User = get_user_model()

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    # User information (can be null for guest checkout)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Guest information
    guest_email = models.EmailField(blank=True, null=True)
    guest_name = models.CharField(max_length=255, blank=True, null=True)
    guest_phone = models.CharField(max_length=15, default="000-000-0000")
    
    # Location information with defaults
    address = models.TextField(default="Address not provided")
    city = models.CharField(max_length=100, default="City not provided")
    state = models.CharField(max_length=100, default="State not provided")
    country = models.CharField(max_length=100, default='United States')
    zip_code = models.CharField(max_length=20, default="00000")
    
    # Location coordinates from Google Maps
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Order details
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if self.user:
            return f"Order #{self.id} - {self.user.email}"
        else:
            return f"Order #{self.id} - {self.guest_email or 'Guest'}"
    
    class Meta:
        ordering = ['-created_at']

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    @property
    def total_price(self):
        return self.quantity * self.price
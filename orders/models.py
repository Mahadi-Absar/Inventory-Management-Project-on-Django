from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

from inventory.models import ProductVariant


class Customer(models.Model):
    """Extends Django's built-in User with T-shirt-shop-specific fields (OneToOne)."""
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='customer_profile'
    )
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    loyalty_points = models.PositiveIntegerField(default=0)

    def __str__(self):
        full_name = self.user.get_full_name()
        return full_name if full_name else self.user.username


class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name='orders'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    shipping_address = models.TextField()
    order_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-order_date']

    def __str__(self):
        return f"Order #{self.id} - {self.customer}"

    @property
    def total_amount(self):
        return sum(item.subtotal for item in self.items.all())


class OrderItem(models.Model):
    """Line item. Order <-> ProductVariant, essentially a many-to-many with extra data."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_variant = models.ForeignKey(
        ProductVariant, on_delete=models.PROTECT, related_name='order_items'
    )
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    class Meta:
        unique_together = ('order', 'product_variant')

    def __str__(self):
        return f"{self.quantity} x {self.product_variant}"
    
    
    def save(self, *args, **kwargs):
        if self.unit_price is None:
            self.unit_price = self.product_variant.product.price
        super().save(*args, **kwargs)

    @property
    def subtotal(self):
        return self.quantity * self.unit_price

    def clean(self):
        if self.product_variant_id and self.quantity > self.product_variant.stock_quantity:
            raise ValidationError({'quantity': 'Not enough stock available for this variant.'})

from django.core.exceptions import ValidationError
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=150)
    contact_email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=11)
    address = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Free-form labels, e.g. Cotton, Summer Collection, Limited Edition."""
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    """A T-shirt design. Actual stock is tracked per size/color in ProductVariant."""
    name = models.CharField(max_length=150)
    sku = models.CharField(max_length=30, unique=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='products'
    )
    supplier = models.ForeignKey(
        Supplier, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='products'
    )
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='products')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.sku})"

    def clean(self):
        if self.price is not None and self.price <= 0:
            raise ValidationError({'price': 'Price must be a positive value.'})


class ProductVariant(models.Model):
    """A specific size/color combination of a Product, with its own stock count."""
    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'X-Large'),
        ('XXL', 'XX-Large'),
    ]

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='variants'
    )
    size = models.CharField(max_length=5, choices=SIZE_CHOICES)
    color = models.CharField(max_length=30)
    stock_quantity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('product', 'size', 'color')
        ordering = ['product', 'size']

    def __str__(self):
        return f"{self.product.name} - {self.size}/{self.color}"

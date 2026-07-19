from django.contrib.auth.models import User
from rest_framework import serializers

from inventory.models import ProductVariant
from inventory.serializers import ProductVariantSerializer

from .models import Customer, Order, OrderItem


class UserMiniSerializer(serializers.ModelSerializer):
    """Minimal nested representation of the built-in User, used read-only inside Customer."""
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class CustomerSerializer(serializers.ModelSerializer):
    # Nested read-only user info
    user = UserMiniSerializer(read_only=True)
    # Sensitive/internal write path: accept a user_id on create, never expose it as writable "user"
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='user', write_only=True
    )

    class Meta:
        model = Customer
        fields = ['id', 'user', 'user_id', 'phone_number', 'address', 'loyalty_points']
        read_only_fields = ['loyalty_points']


class OrderItemSerializer(serializers.ModelSerializer):
    product_variant_detail = ProductVariantSerializer(source='product_variant', read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'id', 'order', 'product_variant', 'product_variant_detail',
            'quantity', 'unit_price', 'subtotal',
        ]
        extra_kwargs = {
            'order': {'write_only': True},
        }

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be at least 1.")
        return value

    def validate(self, attrs):
        variant = attrs.get('product_variant') or getattr(self.instance, 'product_variant', None)
        quantity = attrs.get('quantity') or getattr(self.instance, 'quantity', None)
        if variant and quantity and quantity > variant.stock_quantity:
            raise serializers.ValidationError(
                {'quantity': f"Only {variant.stock_quantity} units left in stock for this variant."}
            )
        return attrs


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    customer_name = serializers.CharField(source='customer.__str__', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'customer', 'customer_name', 'status', 'shipping_address',
            'order_date', 'items', 'total_amount',
        ]
        read_only_fields = ['order_date']

    def validate_shipping_address(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError(
                "Shipping address seems too short - please provide full details."
            )
        return value

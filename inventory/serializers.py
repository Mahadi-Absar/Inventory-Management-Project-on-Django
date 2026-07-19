from rest_framework import serializers

from .models import Category, Product, ProductVariant, Supplier, Tag


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'contact_email', 'phone_number', 'address']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'product', 'size', 'color', 'stock_quantity']
        # 'product' is write-only here because variants are usually nested
        # under a product; it stays writable so variants can also be
        # created directly through /api/variants/.
        extra_kwargs = {
            'stock_quantity': {'min_value': 0},
        }

    def validate_stock_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock quantity cannot be negative.")
        return value


class ProductSerializer(serializers.ModelSerializer):
    # Nested read-only representation of variants under a product
    variants = ProductVariantSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True, required=False
    )

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'sku', 'category', 'category_name', 'supplier',
            'price', 'description', 'tags', 'is_active', 'created_at',
            'variants',
        ]
        read_only_fields = ['created_at']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value

    def validate_sku(self, value):
        if not value.strip():
            raise serializers.ValidationError("SKU cannot be blank.")
        return value.upper()

    def validate(self, attrs):
        # Cross-field / business rule validation example
        category = attrs.get('category', getattr(self.instance, 'category', None))
        name = attrs.get('name', getattr(self.instance, 'name', None))
        if category and name:
            qs = Product.objects.filter(category=category, name__iexact=name)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError(
                    {'name': 'A product with this name already exists in this category.'}
                )
        return attrs

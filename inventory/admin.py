from django.contrib import admin

from .models import Category, Product, ProductVariant, Supplier, Tag


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'contact_email', 'phone_number']
    search_fields = ['name', 'contact_email']
    ordering = ['name']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'sku', 'category', 'supplier', 'price', 'is_active', 'created_at']
    list_filter = ['category', 'supplier', 'is_active']
    search_fields = ['name', 'sku']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    filter_horizontal = ['tags']
    inlines = [ProductVariantInline]


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'size', 'color', 'stock_quantity']
    list_filter = ['size']
    search_fields = ['product__name', 'color']
    ordering = ['product', 'size']

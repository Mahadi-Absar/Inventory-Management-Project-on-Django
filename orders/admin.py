from django.contrib import admin

from .models import Customer, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = []


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'phone_number', 'loyalty_points']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
    ordering = ['user__username']
    readonly_fields = ['loyalty_points']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'status', 'order_date', 'total_amount']
    list_filter = ['status', 'order_date']
    search_fields = ['customer__user__username', 'shipping_address']
    ordering = ['-order_date']
    readonly_fields = ['order_date']
    inlines = [OrderItemInline]

    def total_amount(self, obj):
        return obj.total_amount


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product_variant', 'quantity', 'unit_price']
    list_filter = ['order__status']
    search_fields = ['product_variant__product__name']
    ordering = ['order']

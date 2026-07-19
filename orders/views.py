from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from .models import Customer, Order, OrderItem
from .serializers import CustomerSerializer, OrderItemSerializer, OrderSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.select_related('user')
    serializer_class = CustomerSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'phone_number']
    ordering_fields = ['loyalty_points']


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related('customer', 'customer__user').prefetch_related('items')
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'customer']
    search_fields = ['shipping_address']
    ordering_fields = ['order_date']


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.select_related('order', 'product_variant')
    serializer_class = OrderItemSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['order', 'product_variant']
    ordering_fields = ['quantity']

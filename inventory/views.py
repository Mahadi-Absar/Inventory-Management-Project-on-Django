from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from .filters import ProductFilter
from .models import Category, Product, ProductVariant, Supplier, Tag
from .serializers import (
    CategorySerializer, ProductSerializer, ProductVariantSerializer,
    SupplierSerializer, TagSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'contact_email']
    ordering_fields = ['name']


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category', 'supplier').prefetch_related('tags', 'variants')
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'sku', 'description']
    ordering_fields = ['price', 'created_at', 'name']


class ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.select_related('product')
    serializer_class = ProductVariantSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    filterset_fields = ['product', 'size', 'color']
    search_fields = ['color']
    ordering_fields = ['stock_quantity']

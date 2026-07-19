from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, ProductVariantViewSet, ProductViewSet, SupplierViewSet, TagViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('suppliers', SupplierViewSet, basename='supplier')
router.register('tags', TagViewSet, basename='tag')
router.register('products', ProductViewSet, basename='product')
router.register('variants', ProductVariantViewSet, basename='productvariant')

urlpatterns = router.urls

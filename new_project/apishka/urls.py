from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, CategoryViewSet, ManufacturerViewSet, ArtistViewSet,
    VinylRecordViewSet, OrderViewSet, CartViewSet, OrderDetailViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'manufacturers', ManufacturerViewSet)
router.register(r'artists', ArtistViewSet)
router.register(r'vinyls', VinylRecordViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'carts', CartViewSet)
router.register(r'order-details', OrderDetailViewSet)

urlpatterns = []
urlpatterns += router.urls
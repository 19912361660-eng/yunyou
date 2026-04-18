"""Product URL configuration"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, ExchangeRecordViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('', ProductViewSet, basename='products')
router.register('exchanges', ExchangeRecordViewSet, basename='exchanges')

urlpatterns = [
    path('', include(router.urls)),
]

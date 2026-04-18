"""Attraction URL configuration"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import AttractionViewSet, RouteViewSet, RouteDayViewSet, RouteAttractionViewSet

router = DefaultRouter()
router.register('', AttractionViewSet, basename='attractions')
router.register('routes', RouteViewSet, basename='routes')
router.register('route-days', RouteDayViewSet, basename='route-days')
router.register('route-attractions', RouteAttractionViewSet, basename='route-attractions')

urlpatterns = [
    path('', include(router.urls)),
]

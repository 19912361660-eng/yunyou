"""Backup URL configuration"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BackupViewSet, RestoreViewSet, DataStatsView

router = DefaultRouter()
router.register('backups', BackupViewSet, basename='backups')
router.register('restores', RestoreViewSet, basename='restores')
router.register('stats', DataStatsView, basename='data-stats')

urlpatterns = [
    path('', include(router.urls)),
]

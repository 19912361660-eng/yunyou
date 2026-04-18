"""AI Assistant URL configuration"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatSessionViewSet, ChatMessageViewSet

router = DefaultRouter()
router.register('sessions', ChatSessionViewSet, basename='chat-sessions')
router.register('messages', ChatMessageViewSet, basename='chat-messages')

urlpatterns = [
    path('', include(router.urls)),
]

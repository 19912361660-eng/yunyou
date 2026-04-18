"""User permissions"""
from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """Allow access only to admin users"""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'admin'


class IsOwnerOrAdmin(permissions.BasePermission):
    """Allow access to owner or admin"""
    
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return obj == request.user


class IsActiveUser(permissions.BasePermission):
    """Allow access only to active users"""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.status == 'active'

from rest_framework import permissions
from django.shortcuts import redirect
from rest_framework.exceptions import PermissionDenied

class CustomIsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
class IsManagerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        
        if not request.user or not request.user.is_authenticated:
            return False

        
        is_manager = request.user.groups.filter(name='Manager').exists()
        is_admin = request.user.is_staff or request.user.is_superuser

        if not is_manager and not is_admin:
            raise PermissionDenied("You are not authorized to access this resource.")

        return is_manager or is_admin
    
        
    
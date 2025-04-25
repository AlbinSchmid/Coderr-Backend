from rest_framework.permissions import BasePermission, SAFE_METHODS
from .exeptions import Unauthorized, UserIsNotOwner
__all__ = ['IsOwnerOrAdmin', 'IsAuthenticated']


class IsOwnerOrAdmin(BasePermission):
    """
    Custom permission to only allow owners of an object or superusers to edit it.
    """
    def has_object_permission(self, request, view, obj):
        """
        Check if the request is a safe method (GET, HEAD, OPTIONS) or if the user is the owner of the object.
        """
        if request.method in SAFE_METHODS:
            if request.user and request.user.is_authenticated:
                return True
            raise Unauthorized() 
        elif request.method == 'DELETE':
            if request.user and request.user.is_superuser:
                return True
            raise Unauthorized()
        elif request.user and request.user == obj.user:
            return True
        raise UserIsNotOwner()
    

class IsAuthenticated(BasePermission):
    """
    Custom permission to only allow authenticated users to access the view.
    """
    def has_permission(self, request, view):
        """
        Check if the request is a safe method (GET, HEAD, OPTIONS) or if the user is authenticated.
        """
        if request.method in SAFE_METHODS:
            if request.user and request.user.is_authenticated:
                return True
            raise Unauthorized()
        raise Unauthorized()
        
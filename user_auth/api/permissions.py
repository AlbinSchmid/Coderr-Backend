from rest_framework.permissions import BasePermission, SAFE_METHODS
from .exeptions import Unauthorized
from rest_framework.exceptions import PermissionDenied

class IsOwnerOrAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):
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
        raise Unauthorized()
        
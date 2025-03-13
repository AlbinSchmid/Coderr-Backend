from rest_framework.permissions import BasePermission, SAFE_METHODS
from .exeptions import *

class isAuthenticated(BasePermission):

    def has_permission(self, request, view):
        
        if request.method in SAFE_METHODS:
            if request.user and request.user.is_authenticated:
                return True
            raise UserUnauthenticated
        elif request.method == 'POST':
            if request.user and request.user.is_authenticated:
                return True
            raise UserUnauthenticatedPost

    
class OwnerForDeleteAndPatch(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_authenticated:            
            if request.method == 'DELETE':
                if request.user and request.user == obj.reviewer:
                    return True
                raise UserIsNotOwnerForDelete
                    
            if request.method == 'PATCH':
                if request.user and request.user == obj.reviewer:
                    return True
                raise UserIsNotOwnerForPatch
        raise UserUnauthenticated


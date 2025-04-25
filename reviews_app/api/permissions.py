from rest_framework.permissions import BasePermission, SAFE_METHODS
from .exeptions import *
from user_auth.models import Consumer

class isAuthenticated(BasePermission):
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
            raise UserUnauthenticated
        elif request.method == 'POST':
            if request.user and request.user.is_authenticated:
                consumer_user = Consumer.objects.filter(user__id=request.user.id)
                if consumer_user:
                    return True
                raise UserUnauthenticatedPost
            raise UserUnauthenticatedPost

    
class OwnerForDeleteAndPatch(BasePermission):
    """
    Custom permission to only allow the owner of the review to delete or edit it.
    """
    def has_object_permission(self, request, view, obj):
        """
        Check if the request is a safe method (GET, HEAD, OPTIONS) or if the user is the owner of the review.
        """
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


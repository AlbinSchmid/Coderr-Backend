from rest_framework.permissions import BasePermission, SAFE_METHODS
from .exeptions import *
from user_auth.models import Consumer

class isAuthenticated(BasePermission):

    def has_permission(self, request, view):
        
        if request.method in SAFE_METHODS:
            if request.user and request.user.is_authenticated:
                return True
            raise UserUnauthenticated
        elif request.method == 'POST':
            consumer_user = Consumer.objects.filter(user__id=request.user.id)
            if request.user and request.user.is_authenticated:
                if consumer_user:
                    return True
                raise UserHasAlreadyReview
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


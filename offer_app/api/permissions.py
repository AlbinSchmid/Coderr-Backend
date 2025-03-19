from rest_framework.permissions import BasePermission, SAFE_METHODS
from user_auth.models import Seller
from user_auth.api.exeptions import Unauthorized 
from .exeptions import *

class SellerUserCreateOrReadOnly(BasePermission):
    
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        elif request.method == 'POST':
            if request.user.is_authenticated:
                seller_user = Seller.objects.filter(user__username = request.user.username).first()
                if seller_user:
                    return True
                else:
                    raise NoSellerUser
            raise Unauthorized
        
class OwnerPatchAndDeleteOrIsAuthenticated(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_authenticated:
            if request.method in SAFE_METHODS:
                return True
            elif request.method == 'PATCH' or request.method == 'DELETE':
                if request.user and obj and request.user == obj.user:
                    return True  
                raise UserIsNotOwnerOffer
        raise Unauthorized  
    
class Authenticated(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            if request.user and request.user.is_authenticated:
                return True
            raise Unauthorized
                

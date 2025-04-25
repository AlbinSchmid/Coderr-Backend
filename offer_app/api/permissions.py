from rest_framework.permissions import BasePermission, SAFE_METHODS
from user_auth.models import Seller
from user_auth.api.exeptions import Unauthorized 
from .exeptions import *

class SellerUserCreateOrReadOnly(BasePermission):
    """
    Custom permission to only allow authenticated sellers to create offers.
    All users can read offers.
    """
    def has_permission(self, request, view):
        """
        Check if the user is authenticated and has permission to create offers.
        Sellers are allowed to create offers, while all users can read offers.
        """
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
    """
    Custom permission to only allow the owner of an offer to update or delete it.
    All authenticated users can read offers.
    """
    def has_object_permission(self, request, view, obj):
        """
        Check if the user is the owner of the offer or if they are authenticated.
        """
        if request.user and request.user.is_authenticated:
            if request.method in SAFE_METHODS:
                return True
            elif request.method == 'PATCH' or request.method == 'DELETE':
                if request.user and obj and request.user == obj.user:
                    return True  
                raise UserIsNotOwnerOffer
        raise Unauthorized  
    
class Authenticated(BasePermission):
    """
    Custom permission to only allow authenticated users to access the API.
    """
    def has_permission(self, request, view):
        """
        Check if the user is authenticated.
        """
        if request.method == 'GET':
            if request.user and request.user.is_authenticated:
                return True
            raise Unauthorized
                

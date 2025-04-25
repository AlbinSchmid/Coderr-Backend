from rest_framework.permissions import BasePermission, SAFE_METHODS
from user_auth.models import Consumer, Seller
from .exeptions import *
from user_auth.api.exeptions import Unauthorized
from order_app.models import Order

class ConsumerForPostOrAuthenticated(BasePermission):
    """
    Custom permission to only allow authenticated users to create orders.
    Consumers are allowed to create orders, while sellers and staff members are not.
    """
    def has_permission(self, request, view):
        """
        Check if the user is authenticated and has permission to create orders.
        """
        if request.user and request.user.is_authenticated:
            if request.method in SAFE_METHODS:
                return True
            elif request.method == 'POST':
                consumer_user = Consumer.objects.filter(user__username=request.user.username).first()
                if consumer_user:
                    return True
                raise UserIsNotConsumer
        raise Unauthorized
                

class SellerForPatchOrStaffForDelete(BasePermission):
    """
    Custom permission to only allow sellers to update orders and staff members to delete orders.
    """
    def has_permission(self, request, view):
        """
        Check if the user is authenticated and has permission to update or delete orders.
        Sellers are allowed to update orders, while staff members are allowed to delete orders.
        """
        if request.user and request.user.is_authenticated:
            if request.method == 'PATCH':
                seller_user = Seller.objects.filter(user__username=request.user.username).first()
                obj_pk = view.kwargs.get('pk')
                obj = Order.objects.filter(id=obj_pk).first()
                if obj is None:
                    raise OrderNotFound
                if seller_user:
                    return True
                raise UserIsNotSeller
            elif request.method == 'DELETE':
                if request.user and request.user.is_staff:
                    return True
                raise UserIsNotStaff
        raise Unauthorized

from rest_framework.permissions import BasePermission, SAFE_METHODS
from user_auth.models import Consumer, Seller
from .exeptions import *
from user_auth.api.exeptions import Unauthorized
from order_app.models import Order

class ConsumerForPostOrAuthenticated(BasePermission):
    
    def has_permission(self, request, view):
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

    def has_permission(self, request, view):
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

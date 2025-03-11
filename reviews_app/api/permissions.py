from rest_framework.permissions import BasePermission, SAFE_METHODS
from .exeptions import *

class IsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            if request.method in SAFE_METHODS or request.method == 'POST':
                return True
        raise UserUnauthenticated


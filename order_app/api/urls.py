from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('orders/', OrderListView.as_view(), name='orders'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order'),
    path('order-count/<int:pk>/', OrderListView.as_view(), name='order-count'),
    path('completed-oder-count/<int:pk>/', OrderListView.as_view(), name='complete-order-count'),
]
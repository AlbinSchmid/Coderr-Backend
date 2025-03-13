from django.urls import path
from .views import *

urlpatterns = [
    path('base-info/', BaseInfoView.as_view(), name='orders'),
]
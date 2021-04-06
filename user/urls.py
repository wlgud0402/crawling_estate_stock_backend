from django.urls import path
from .api import UserAPI, UserInfoAPI
from rest_framework import generics

urlpatterns = [
    path('', UserAPI.as_view(), name='user'),
    path('info/', UserInfoAPI.as_view(), name='user_info'),
]

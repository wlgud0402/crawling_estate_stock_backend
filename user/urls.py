from django.urls import path
from .api import UserAPI, UserInfoAPI, UserDeleteAPI
from rest_framework import generics

urlpatterns = [
    path('', UserAPI.as_view(), name='user'),
    path('delete/', UserDeleteAPI.as_view(), name='user_delete'),
    path('info/', UserInfoAPI.as_view(), name='user_info'),
]

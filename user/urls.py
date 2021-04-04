from django.urls import path
from .api import UserAPI
from rest_framework import generics

urlpatterns = [
    path('', UserAPI.as_view(), name='user'),
]

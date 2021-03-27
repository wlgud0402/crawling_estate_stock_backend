from django.urls import path
from .views import log_check
urlpatterns = [
    path('', log_check, name='log_check')
]

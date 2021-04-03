from django.urls import path
from .views import send_mail_estate, send_mail_stock, send_mail_stock_detail
urlpatterns = [
    path('send/estate/', send_mail_estate, name='send_mail_estate'),
    path('send/stock/', send_mail_stock, name='send_mail_stock'),
    path('send/stock/detail/', send_mail_stock_detail,
         name='send_mail_stock_detail'),
]

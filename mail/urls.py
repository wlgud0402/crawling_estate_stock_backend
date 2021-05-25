from django.urls import path
from .views import send_mail_estate_by_celery, \
    send_mail_stock_detail_by_celery, \
    send_mail_stock_by_celery

urlpatterns = [
    path('send/estate/', send_mail_estate_by_celery,
         name='send_mail_estate_by_celery'),
    # path('send/stock/', send_mail_stock, name='send_mail_stock'),
    path('send/stock/', send_mail_stock_by_celery,
         name='send_mail_stock_by_celery'),
    path('send/stock/detail/', send_mail_stock_detail_by_celery,
         name='send_mail_stock_detail_by_celery'),
]

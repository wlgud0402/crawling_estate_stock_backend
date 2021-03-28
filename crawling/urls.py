from django.urls import path
from .views import crawl_estate, crawl_stock_trend, crawl_stock_detail, crawl_stock_draw
urlpatterns = [
    path('estate/', crawl_estate, name='crawl_state'),
    path('stock/trend/', crawl_stock_trend, name='crawl_stock_trend'),
    path('stock/detail/', crawl_stock_detail, name='crawl_stock_detail'),
    path('stock/detail/draw/', crawl_stock_draw, name='crawl_stock_draw'),
]

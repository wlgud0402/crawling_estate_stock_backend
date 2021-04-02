from django.db import models
from django.core.cache import cache

# Create your models here.


class Estate(models.Model):
    location = models.CharField("검색한지역", max_length=254)
    estate_data = models.JSONField("부동산정보", null=True, blank=True)
    create_at = models.DateTimeField("생성시간", auto_now_add=True)
    modified_at = models.DateTimeField("수정시간", auto_now=True)

    def __str__(self):
        return self.location


class StockTrend(models.Model):
    sosok = models.CharField("코스피 / 코스닥", max_length=254)
    page = models.IntegerField("페이지수")
    trend_data = models.JSONField("주식트랜드", null=True, blank=True)
    create_at = models.DateTimeField("생성시간", auto_now_add=True)
    modified_at = models.DateTimeField("수정시간", auto_now=True)

    def __str__(self):
        return self.sosok


class StockDetail(models.Model):
    stock_name = models.CharField("주식이름", max_length=254)
    detail_data = models.JSONField("주식트랜드", null=True, blank=True)
    create_at = models.DateTimeField("생성시간", auto_now_add=True)
    modified_at = models.DateTimeField("수정시간", auto_now=True)

    def __str__(self):
        return self.stock_name

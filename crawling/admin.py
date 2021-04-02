from django.contrib import admin
from .models import Estate, StockTrend, StockDetail


# Register your models here.
@admin.register(Estate)
class EstateAdmin(admin.ModelAdmin):
    list_display = ('location', 'create_at', 'modified_at',)


@admin.register(StockTrend)
class StockTrendAdmin(admin.ModelAdmin):
    list_display = ('sosok', 'page', 'create_at', 'modified_at',)


@admin.register(StockDetail)
class StockDetailAdmin(admin.ModelAdmin):
    list_display = ('stock_name', 'create_at', 'modified_at',)

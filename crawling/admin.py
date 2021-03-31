from django.contrib import admin
from .models import Estate


# Register your models here.
@admin.register(Estate)
class EstateAdmin(admin.ModelAdmin):
    list_display = ('location', 'create_at', 'modified_at',)

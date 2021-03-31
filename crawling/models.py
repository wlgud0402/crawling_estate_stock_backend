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

    # def save(self, *args, **kwargs):
    #     cache.delete(self.location)
    #     super().save(*args, **kwargs)

    # def delete(self, *args, **kwargs):
    #     cache.delete(self.location)
    #     super().delete(*args, **kwargs)

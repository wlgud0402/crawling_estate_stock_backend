from django.db import models
from user.models import User

# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField("글 제목", max_length=254)
    text = models.CharField("글 내용", max_length=254)
    created_at = models.DateTimeField("생성시간", auto_now_add=True)

    def get_username(self):
        return self.user.nickname

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name='comments')
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    content = models.CharField("댓글내용", max_length=254)
    created_at = models.DateTimeField("생성시간", auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.user.nickname

from django.db import models

# Create your models here.


class User(models.Model):
    google_id = models.CharField(
        ("구글로그인 아이디"), max_length=254)
    email = models.EmailField(
        ("사용자 이메일"), max_length=254)
    nickname = models.CharField(("닉네임"), max_length=254)
    use_count = models.IntegerField(("방번호"), null=True, default=0)
    created_at = models.DateTimeField(("가입일"), auto_now_add=True)

    def __str__(self):
        return self.nickname

    def get_nickname(self):
        return self.nickname

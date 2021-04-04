# Generated by Django 3.1 on 2021-04-03 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('google_id', models.CharField(max_length=254, verbose_name='구글로그인 아이디')),
                ('email', models.EmailField(max_length=254, verbose_name='사용자 이메일')),
                ('nickname', models.CharField(max_length=254, verbose_name='닉네임')),
                ('use_count', models.IntegerField(default=0, null=True, verbose_name='방번호')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='가입일')),
            ],
        ),
    ]

# Generated by Django 3.1 on 2021-03-31 12:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crawling', '0006_stocktrend'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stocktrend',
            old_name='trend_page',
            new_name='page',
        ),
        migrations.RenameField(
            model_name='stocktrend',
            old_name='trend_kind',
            new_name='sosok',
        ),
    ]

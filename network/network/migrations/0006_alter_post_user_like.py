# Generated by Django 3.2.5 on 2021-10-21 10:27

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_auto_20211021_1012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='user_like',
            field=models.ManyToManyField(blank=True, related_name='liked', to=settings.AUTH_USER_MODEL),
        ),
    ]

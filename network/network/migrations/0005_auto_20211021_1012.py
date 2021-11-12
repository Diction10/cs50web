# Generated by Django 3.2.5 on 2021-10-21 09:12

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_auto_20211021_0814'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='user_like',
            field=models.ManyToManyField(blank=True, related_name='like', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='post',
            name='like',
        ),
        migrations.AddField(
            model_name='post',
            name='like',
            field=models.IntegerField(default=0),
        ),
    ]

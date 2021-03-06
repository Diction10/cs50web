# Generated by Django 3.2.5 on 2021-10-21 07:14

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_profile_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='has_liked',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='liked_on',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='post',
        ),
        migrations.AddField(
            model_name='post',
            name='has_liked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='liked_on',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.RemoveField(
            model_name='post',
            name='like',
        ),
        migrations.AddField(
            model_name='post',
            name='like',
            field=models.ManyToManyField(blank=True, related_name='like', to=settings.AUTH_USER_MODEL),
        ),
    ]

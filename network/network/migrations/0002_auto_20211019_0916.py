# Generated by Django 3.2.5 on 2021-10-19 08:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='has',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='posts',
        ),
    ]
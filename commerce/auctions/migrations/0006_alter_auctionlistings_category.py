# Generated by Django 3.2.5 on 2021-08-22 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_alter_auctionlistings_item_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlistings',
            name='category',
            field=models.CharField(choices=[('electronics', 'ELECTRONICS'), ('fabric', 'FABRIC'), ('consumable', 'CONSUMABLE'), ('estate', 'ESTATE'), ('othes', 'OTHERS')], default='Choose One', max_length=100),
        ),
    ]

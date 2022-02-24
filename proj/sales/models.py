from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

from django.db.models.signals import post_save
from django.dispatch import receiver
from erp.models import User
from datetime import datetime


class Product(models.Model):
    name = models.CharField(max_length=255, blank=True,
                            null=False, unique=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.IntegerField()
    on_sale = models.BooleanField(default=True)
    date_created = models.DateField(default=datetime.now, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # image = models.ImageField(default='default.jpg', upload_to='listing_img')

    def __str__(self):
        # return self.item_name
        return f'{self.name}'

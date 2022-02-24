from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class User(AbstractUser):
    SEX_CHOICES = (
        ('default', 'Select Sex'),
        ('Male', 'Male',),
        ('Female', 'Female',),
        ('Unsure', 'Unsure',),
    )
    sex = models.CharField(max_length=10, choices=SEX_CHOICES, default='')

    DEPARTMENT_CHOICES = (
        ('default', 'Select Department'),
        ('Accounting', 'Accounting',),
        ('Human Resource', 'Human Resource',),
        ('Sales', 'Sales',),
    )
    department = models.CharField(
        max_length=20, choices=DEPARTMENT_CHOICES, default='')

    leave_days = models.IntegerField(default=15)
    salary = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    # image = models.ImageField(default='default.jpg', upload_to='listing_img')

    # def __str__(self):
    #     # return self.item_name
    #     return f'{self.username}'

from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime
from PIL import Image


class User(AbstractUser):
    pass


CATEGORY_CHOICES = (
    ('default','Select Category'),
    ('electronics','Electronics'),
    ('fabric', 'Fabric'),
    ('consumable','Consumable'),
    ('estate','Estate'),
    ('othes','Others'),
)


class AuctionListings(models.Model):
    item_name = models.CharField(max_length=100)
    item_description = models.TextField(default='')
    item_price = models.DecimalField(max_digits=8, decimal_places=2)
    date_created = models.DateField(default=datetime.now, blank=False)
    item_image = models.ImageField(default='default.jpg', upload_to='listing_img')
    item_url = models.URLField(blank=True)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='default')
    is_active = models.BooleanField(default=True)
    is_closed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        # return self.item_name
        return f'{self.user} created {self.item_name}'

    # to resize the images
    def save(self):
        super().save()

        img = Image.open(self.item_image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.item_image.path)



class Bids(models.Model):
    item_name = models.ForeignKey(AuctionListings, on_delete=models.CASCADE)
    item_bid = models.DecimalField(max_digits=8, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.user} bidded on {self.item_name.item_name} for ${self.item_bid}'



class Comments(models.Model):
    item_name = models.ForeignKey(AuctionListings, on_delete=models.CASCADE)
    item_comment = models.TextField()
    # date_comment = models.DateField(default=datetime.now, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} commented on {self.item_name.item_name}'


class Watchlist(models.Model):
    item_name = models.ForeignKey(AuctionListings, on_delete=models.CASCADE)
    is_added = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.user} added {self.item_name.item_name} to watchlist'
    





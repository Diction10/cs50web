from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from PIL import Image

# from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    pass

class Post(models.Model):
    post_content = models.TextField()
    has_liked = models.BooleanField(default=False)
    user_like = models.ManyToManyField(User, blank=True, related_name='liked')
    liked_on = models.DateTimeField(auto_now=True)
    date_posted = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} posted'


class Profile(models.Model):
    followers = models.ManyToManyField(User, blank=True, related_name='follwers')
    following = models.ManyToManyField(User, blank=True, related_name='following')
    is_following = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pic.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

   


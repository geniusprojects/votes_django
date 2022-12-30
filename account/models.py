from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import PIL
from PIL import Image
import uuid


class Account(models.Model):
    id = models.BigIntegerField(default=0)
    uid = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    avatar = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def new_user(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)
        instance.account.save()


@receiver(post_save, sender=User)
def save_user_account(sender, instance, created, **kwargs):
    if created:
        instance.account.save()


class Pin(models.Model):
    phone = models.CharField(max_length=20)
    pins = models.CharField(max_length=10)
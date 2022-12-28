from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count
from django.db.models.signals import post_save
from django.dispatch import receiver
import PIL
from PIL import Image
import uuid

from account.models import Account
from poll.models import Poll, Vote


class Gallery(models.Model):
    id = models.BigIntegerField(default=0)
    uid = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    poll = models.ForeignKey(Poll, related_name='polls', blank=True, null=True, on_delete=models.CASCADE)
    vote = models.ForeignKey(Vote, related_name='votes', blank=True, null=True, on_delete=models.SET_NULL)
    title = models.CharField('Title', max_length=250)
    path = models.ImageField(upload_to='images')
    main = models.BooleanField('Main image', blank=True, default=False)
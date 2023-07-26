from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count
from django.db.models.signals import post_save
from django.dispatch import receiver
import PIL
from PIL import Image
import uuid

from account.models import Account


class CategoryGroup(models.Model):
    title = models.CharField('Title', max_length=150)
    description = models.TextField('Description', max_length=1000, blank=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    group = models.ForeignKey(CategoryGroup, related_name='categories', on_delete=models.CASCADE)
    title = models.CharField('Title', max_length=150)
    description = models.TextField('Description', max_length=1000, blank=True)

    def __str__(self):
        return self.title

    def less_products(self):
        return Product.objects.filter(category=self)[:4]#.order_by('-choice__vote__updated').annotate(cnt=Count('choice__vote')).order_by('-cnt')[:4]


class Product(models.Model):
    id = models.BigIntegerField(default=0)
    uid = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    account = models.ForeignKey(Account, related_name='products', on_delete=models.CASCADE)
    title = models.CharField('Title', max_length=150)
    description = models.TextField('Description', max_length=5000)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    points = models.FloatField(default=0.00, blank=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', related_name='variants', on_delete=models.CASCADE, blank=True, null=True)

    price = models.FloatField(default=0)
    is_featured = models.BooleanField(default=False)
    num_available = models.IntegerField(default=1)
    num_visits = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def get_images(self):
        from gallery.models import Gallery
        return Gallery.objects.all().filter(product=self).order_by('-id')

    def get_main_images(self):
        from gallery.models import Gallery
        return Gallery.objects.filter(product=self, main=True).first()

    def get_count_points(self):
        points = self.points
        return points

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

    def less_polls(self):
        return Poll.objects.filter(category=self).order_by('-choice__vote__updated').annotate(cnt=Count('choice__vote')).order_by('-cnt')[:4]


class Poll(models.Model):
    id = models.BigIntegerField(default=0)
    uid = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    account = models.ForeignKey(Account, related_name='polls', on_delete=models.CASCADE)
    title = models.CharField('Title', max_length=150)
    description = models.TextField('Description', max_length=5000)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    points = models.FloatField(default=0.00, blank=True)
    category = models.ForeignKey(Category, related_name='polls', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_images(self):
        from gallery.models import Gallery
        return Gallery.objects.all().filter(poll=self).order_by('-id')

    def get_main_images(self):
        from gallery.models import Gallery
        return Gallery.objects.filter(poll=self, main=True).first()

    def get_count_votes(self):
        choices = Choice.objects.filter(poll=self)
        votes = Vote.objects.filter(choice__in=choices).count()
        return votes


class Choice(models.Model):
    id = models.BigIntegerField(default=0)
    uid = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    color = models.CharField(max_length=200)

    def __str__(self):
        return self.choice_text + ' (' + self.poll.title + ')'


class Vote(models.Model):
    id = models.BigIntegerField(default=0)
    uid = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, null=True)
    comment = models.TextField('Comment', max_length=1000, blank=True, null=True)
    #value = models.BooleanField('Value')
    updated = models.DateTimeField(auto_now=True)

    def get_total_likes(self):
        return self.get_likes.accounts.count() if hasattr(self, 'get_likes') else 0

    def get_total_dis_likes(self):
        return self.get_dis_likes.accounts.count() if hasattr(self, 'get_dis_likes') else 0

    def __str__(self):
        return self.choice.choice_text + ' (' + self.choice.poll.title + ')'


class Like(models.Model):
    id = models.BigIntegerField(default=0)
    uid = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    vote = models.OneToOneField(Vote, related_name="get_likes", on_delete=models.CASCADE)
    accounts = models.ManyToManyField(Account, related_name='requirement_comment_likes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.vote.comment)[:30]


class DisLike(models.Model):
    id = models.BigIntegerField(default=0)
    uid = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    vote = models.OneToOneField(Vote, related_name="get_dis_likes", on_delete=models.CASCADE)
    accounts = models.ManyToManyField(Account, related_name='requirement_comment_dis_likes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.vote.comment)[:30]
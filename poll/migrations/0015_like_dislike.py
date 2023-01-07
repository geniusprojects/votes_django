# Generated by Django 4.1.4 on 2023-01-05 21:48

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        ('poll', '0014_remove_like_accounts_remove_like_vote_delete_dislike_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigIntegerField(default=0)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('accounts', models.ManyToManyField(related_name='requirement_comment_likes', to='account.account')),
                ('vote', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='get_likes', to='poll.vote')),
            ],
        ),
        migrations.CreateModel(
            name='DisLike',
            fields=[
                ('id', models.BigIntegerField(default=0)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('accounts', models.ManyToManyField(related_name='requirement_comment_dis_likes', to='account.account')),
                ('vote', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='get_dis_likes', to='poll.vote')),
            ],
        ),
    ]

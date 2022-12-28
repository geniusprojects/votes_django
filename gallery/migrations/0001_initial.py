# Generated by Django 4.1.4 on 2022-12-17 14:25

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('poll', '0010_remove_vote_value'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigIntegerField(default=0)),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=250, verbose_name='Title')),
                ('path', models.ImageField(upload_to='images')),
                ('main', models.BooleanField(blank=True, default=False, verbose_name='Main image')),
                ('poll', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polls', to='poll.poll')),
                ('vote', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='votes', to='poll.vote')),
            ],
        ),
    ]

# Generated by Django 4.1.4 on 2023-02-26 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0015_like_dislike'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='description',
            field=models.TextField(max_length=5000, verbose_name='Description'),
        ),
    ]
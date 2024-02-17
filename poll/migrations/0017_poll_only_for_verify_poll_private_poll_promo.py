# Generated by Django 4.1.4 on 2023-12-21 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0016_alter_poll_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='poll',
            name='only_for_verify',
            field=models.BooleanField(blank=True, default=False, verbose_name='Only For Verify Users'),
        ),
        migrations.AddField(
            model_name='poll',
            name='private',
            field=models.BooleanField(blank=True, default=False, verbose_name='Private Poll'),
        ),
        migrations.AddField(
            model_name='poll',
            name='promo',
            field=models.BooleanField(blank=True, default=False, verbose_name='Promo Poll'),
        ),
    ]
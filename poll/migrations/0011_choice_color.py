# Generated by Django 3.2.16 on 2023-01-04 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0010_remove_vote_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='color',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]

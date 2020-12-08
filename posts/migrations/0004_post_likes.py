# Generated by Django 3.1.3 on 2020-12-01 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('likes', '0002_auto_20201201_0720'),
        ('posts', '0003_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(through='posts.Like', to='likes.Like'),
        ),
    ]

# Generated by Django 3.1.3 on 2020-12-01 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('likes', '0001_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='like',
            index=models.Index(fields=['id'], name='likes_like_id_39c1f7_idx'),
        ),
    ]

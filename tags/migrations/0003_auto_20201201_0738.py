# Generated by Django 3.1.3 on 2020-12-01 07:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0002_auto_20201201_0720'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tag',
            name='updated_on',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
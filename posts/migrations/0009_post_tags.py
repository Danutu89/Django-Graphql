# Generated by Django 3.1.3 on 2020-12-01 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0003_auto_20201201_0738'),
        ('posts', '0008_auto_20201201_0749'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(to='tags.Tag'),
        ),
    ]

# Generated by Django 4.2.5 on 2023-09-18 19:27

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appuser', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='friends',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='appuser',
            name='picture_path',
            field=models.ImageField(blank=True, null=True, upload_to='media/profile_pics/'),
        ),
    ]

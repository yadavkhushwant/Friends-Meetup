# Generated by Django 4.2.5 on 2023-09-18 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appuser', '0002_appuser_friends_alter_appuser_picture_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='picture_path',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics/'),
        ),
    ]

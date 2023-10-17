from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class AppUser(AbstractUser):

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    user_name_sequence = models.CharField(max_length=40)
    full_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    address = models.CharField(max_length=255)
    pin_code = models.CharField(max_length=10)
    picture_path = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    # Many-to-many relationship for friends
    friends = models.ManyToManyField('self', blank=True)
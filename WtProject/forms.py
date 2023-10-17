from django import forms
from appuser.models import AppUser
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    class Meta:
        model = AppUser
        fields = ('full_name', 'email', 'password1', 'password2', 'address', 'pin_code', 'gender', 'picture_path')

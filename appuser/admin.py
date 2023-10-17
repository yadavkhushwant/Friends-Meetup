from django.contrib import admin

from appuser.models import AppUser

# Register your models here.
class appUser_admin(admin.ModelAdmin):
    list_display = ('id','password','last_login','is_superuser','username','first_name','last_name','email','is_staff','is_active','date_joined','user_name_sequence','full_name','gender','address','pin_code','picture_path')

admin.site.register(AppUser,appUser_admin)

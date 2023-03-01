from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models.user import User 

class CustomUser(UserAdmin):
    pass

admin.site.register(User, CustomUser)

# Register your models here.

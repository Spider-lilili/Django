from django.contrib import admin
from user.models import *

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'sex', 'birthday', 'phone', 'last_login', 'is_active']
    search_fields = ['username', 'email', 'phone']
    ordering = ['id']



admin.site.register(UserProfile, UserAdmin)
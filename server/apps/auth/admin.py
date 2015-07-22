from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from models import *


class UserProfileInline(admin.TabularInline):
    model = UserProfile
    fk_name = 'user'
    max_num = 1

# Define a new UserAdmin class


class AdminUserAdmin(UserAdmin):
    inlines = [UserProfileInline, ]

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, AdminUserAdmin)

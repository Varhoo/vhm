from models import *
from django.contrib import admin

admin.site.register(SvnUserRights)


class RightsInline(admin.TabularInline):
    model = SvnUserRights
    extra = 0


class SvnRepositoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'users')
    inlines = [RightsInline, ]

admin.site.register(SvnRepository, SvnRepositoryAdmin)

from models import *
from django.contrib import admin


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'priority', 'created', 'deadline', 'get_members')

admin.site.register(Project, ProjectAdmin)

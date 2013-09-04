from models import *
from django.contrib import admin

class TaskPeriodAdmin(admin.ModelAdmin):
    list_display = ('title', 'cron', 'is_enable', 'get_previous_run', 'date_last', 'date_start')

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'common', 'date_run', 'get_time_long')

admin.site.register(Task, TaskAdmin)
admin.site.register(TaskPeriod, TaskPeriodAdmin)

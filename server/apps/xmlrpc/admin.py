# coding: utf-8
# Author: Pavel Studeník
# Email: studenik@varhoo.cz
# Date: 10.8.2014

from models import *
from django.contrib import admin
from apps.xmlrpc.models import *


class ActionServerAdmin(admin.ModelAdmin):
    list_display = ('server', 'command', 'status', 'exit_code', 'last_modify')
    list_filter = ('server__hostname', 'status')
    search_fields = ("command", )
    readonly_fields = ( "result", "exit_code", "last_modify")
    fieldsets = (
        (None, {
            'fields':
                (('server', 'last_modify'), ('status', 'command_type'), "command", "result", "exit_code" )
        }),
        #('Advanced options', {
        #    'classes': ('collapse',),
        #    'fields': ('last_modify',)
        #}),
    )

    def save_model(self, request, obj, form, change):
        obj.status = 0
        obj.save()

admin.site.register(Action)
admin.site.register(ActionServer,ActionServerAdmin)

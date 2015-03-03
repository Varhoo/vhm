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


admin.site.register(Action)
admin.site.register(ActionServer,ActionServerAdmin)

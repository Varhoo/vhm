from models import *
from django.contrib import admin
from apps.xmlrpc.models import *

class ActionServerAdmin(admin.ModelAdmin):
    list_display = ('server','command','status','exit_code','last_modify')

admin.site.register(Action)
admin.site.register(ActionServer,ActionServerAdmin)

from django.contrib import admin
from django.core.urlresolvers import reverse

from models import *


class RecordAdmin(admin.ModelAdmin):
    list_display = ('server', 'name', 'value', 'datecreated')

admin.site.register(Record, RecordAdmin)

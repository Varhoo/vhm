from django.contrib import admin

from models import *

admin.site.register(Comment)


class CommentInLine(admin.TabularInline):
    model = Comment
    extra = 0


class TicketAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('title', 'text', 'group', ('priority', 'status',), ('author', 'owner'))
        }),)
    inlines = [CommentInLine, ]


class GroupAdmin(admin.ModelAdmin):
    filter_horizontal = ('users',)
    pass

admin.site.register(Ticket, TicketAdmin)
admin.site.register(Group, GroupAdmin)

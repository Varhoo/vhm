#!/usr/bin/python
# coding: utf-8 
# Author: Pavel Studeník
# Email: studenik@varhoo.cz
# Date: 10.2.2010


from models import *
from django.contrib import admin
from django.core.urlresolvers import reverse


class DomainInline(admin.TabularInline):
    model = DomainCommmercial
    extra = 0
    list_display = ('domain', 'get_info', "get_expire")
    readonly_fields = ("get_info", "get_expire")


class InvoiceInline(admin.TabularInline):
    model = Invoice
    extra = 0


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'tel') 
    inlines = [DomainInline, InvoiceInline]


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('account', 'date', 'date_end', 'size', 'price', 'is_paid') 
    fieldsets = (
        (None, {
            'fields':
                ('account', 'user', 'date', ('month', 'size', 'sale'), 'price',
                'is_paid', 'file', )
        }),) 
    readonly_fields = ['price', ]

    def queryset(self, request):
        return Invoice.objects.filter(account__owner=request.user)


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Invoice, InvoiceAdmin)
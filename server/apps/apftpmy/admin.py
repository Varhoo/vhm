from models import *
from django.contrib import admin

admin.site.register(Customer)

class MultiDBModelAdmin(admin.ModelAdmin):
    # A handy constant for the name of the alternate database.
    using = 'proftpd'

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, requqest, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super(MultiDBModelAdmin, self).queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super(MultiDBModelAdmin, self).formfield_for_foreignkey(db_field, request=request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super(MultiDBModelAdmin, self).formfield_for_manytomany(db_field, request=request, using=self.using, **kwargs)


#from django.db import connections
#cursor = connections['ftpuser'].cursor()


class ApacheInline(admin.TabularInline):
    model = ApacheAlias
    extra = 1


class AliasInline(admin.TabularInline):
    model = AccountAlias
    extra = 0


class FtpuserInLine(admin.TabularInline):
    model = Ftpuser
    extra = 0


class FtpuserAdmin(admin.ModelAdmin):
    list_display = ('account', 'homedir')

    
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'path', 'sizeformat', 'account_type', 'last_invoice_date', 'is_pay')
    fieldsets = (
        (None, {
            'fields': 
                ( ('owner', 'account_type'), 'server', 
                'name', 'path', 'size' )
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('user', ('uid','gid'), 'token',)
        }),
    )
    readonly_fields = ['size', 'token' ]
    ordering= ['-account_type',]
    inlines = [FtpuserInLine, ]


class ApacheAliasAdmin(admin.ModelAdmin):
    #list_display = ('account','site','django_wsgi','is_valid','power')
    fieldsets = (
        (None, {
            'fields':
                ('account', 'site', ('django_wsgi', 'is_valid', 'power'), 
                ('repo_type', 'repo_version'), 'repo_url', 'note', 'comment')
        }),)
    inlines = [AliasInline, ]


class InvoiceAdmin(admin.ModelAdmin):
    def price_enum(self, size):
        if size < 10:
            return 49
        else:
            return 19.9

    list_display = ('account', 'date', 'date_end', 'size', 'price', 'is_paid')
    fieldsets = (
        (None, {
            'fields':
                ('account', 'user', 'date', ('month', 'size', 'sale'), 'price',
                'is_paid', 'file', )
        }),)
    ordering = ['-date']
    readonly_fields = ['price', ]

    def save_model(self, request, obj, form, change):
        obj.price = obj.size * obj.month * self.price_enum(obj.size) 
        # discount for order
        obj.price = obj.price * ( 1 - obj.sale/100.0 )
        obj.save()

    
class DomainAdmin(admin.ModelAdmin):
    list_display = ('name','expirate','description','check_pay')
    ordering = ['expirate',]

admin.site.register(ApacheAlias, ApacheAliasAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Ftpuser, FtpuserAdmin)
admin.site.register(Server)
admin.site.register(Domain, DomainAdmin)

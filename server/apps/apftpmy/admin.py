from models import *
from django.contrib import admin
from django.core.urlresolvers import reverse

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


class AliasInline(admin.TabularInline):
    model = DomainAlias
    extra = 0


class ProcInline(admin.TabularInline):
    model = ProjectProc
    extra = 0


class ProjectInline(admin.TabularInline):
    model = ProjectSetting
    extra = 0
    fields = ("get_admin_link", "path", "site", "is_enabled" )
    readonly_fields = ( "get_admin_link", )
    def get_admin_link(self, obj):
        url = reverse('admin:apftpmy_projectsetting_change', args=(obj.pk,))
        return '<a href="%s">1%s</a>' % (url, obj.id)
    get_admin_link.allow_tags = True


class FtpuserInLine(admin.TabularInline):
    model = Ftpuser
    extra = 0


class FtpuserAdmin(admin.ModelAdmin):
    list_display = ('account', 'homedir')

    
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'path', 'sizeformat')
    fieldsets = (
        (None, {
            'fields':
                ( 'owner', 'server', 'name', 'size' )
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('user', "path", ('uid', 'gid'), 'token',)
        }),
    )
    readonly_fields = ['size', 'token', "uid", "gid" ]
    ordering= ['name',]
    inlines = [ProjectInline, FtpuserInLine, ]
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()


class ProjectProcAdmin(admin.ModelAdmin):
    list_display = ('project', "get_account", "template", 'is_enabled', 'is_running')
    fieldsets = (
        (None, {
            'fields':
                ('project', ('template', "is_running"), "params", ("get_raw", "get_template"))
            }),
        )
    readonly_fields = ("is_running", "get_raw", "get_template")

class ProjectSettingAdmin(admin.ModelAdmin):
    list_display = ('account', 'site', 'repo_type', 'last_update', 'is_enabled')
    #fieldsets = (
    #    (None, {
    #        'fields': ('account', 'site', ('django_wsgi','is_valid','power'), ('repo_type','repo_version'), 'repo_url', 'note', 'comment')
    #    }),)
    inlines = [AliasInline, ProcInline ]
    def queryset(self, request):
        return ProjectSetting.objects.filter(account__owner=request.user)
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()


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

    
class DomainAdmin(admin.ModelAdmin):
    list_display = ('name', 'expirate', 'description', 'check_pay')
    ordering = ['expirate',]

    def queryset(self, request):
        return Domain.objects.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()


admin.site.register(Server)
admin.site.register(Customer)
admin.site.register(DomainAlias)
admin.site.register(TemplateProc)
admin.site.register(ProjectProc, ProjectProcAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Ftpuser, FtpuserAdmin)
admin.site.register(ProjectSetting, ProjectSettingAdmin)
admin.site.register(Domain, DomainAdmin)

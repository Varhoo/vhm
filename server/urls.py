# coding: utf-8

from django.conf import settings
from django.conf.urls import include, patterns, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.views.generic import RedirectView
from filebrowser.sites import site

admin.autodiscover()


urlpatterns = patterns('',
                       url(r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:],
                           'django.views.static.serve',
                           {"document_root": settings.MEDIA_ROOT}),

                       url(r'^%s(?P<path>.*)$' % settings.STATIC_URL[1:],
                           'django.views.static.serve',
                           {"document_root": settings.STATIC_ROOT}),

                       # Uncomment the admin/doc line below to enable admin
                       # documentation:
                       (r'^doc/', include('django.contrib.admindocs.urls')),
                       #(r'^openid/', include('apps.consumer.urls')),
                       (r'^$', RedirectView.as_view(url='/admin/')),
                       (r'^ticket/', include('apps.ticket.urls')),
                       #(r'^admin/login/','apps.auth.views.index'),
                       (r'^admin/grappelli/', include('grappelli.urls')),
                       (r'^admin/filebrowser/', include(site.urls)),
                       # Uncomment the next line to enable the admin:
                       (r'^xmlrpc/$', 'apps.xmlrpc.models.rpc_handler'),
                       (r'^admin/', include(admin.site.urls)),
                       )

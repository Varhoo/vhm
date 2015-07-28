from django.conf.urls import *

# Uncomment the next two lines to enable the admin:

urlpatterns = patterns('',
                       # Uncomment the admin/doc line below to enable admin
                       # documentation:
                       url(r'^$', 'apps.ticket.views.show_all',
                           name='tickets_all'),
                       url(r'^id/(?P<id>[0-9]+)$',
                           'apps.ticket.views.show_item', name='ticket_id'),
                       url(r'^new/$', 'apps.ticket.views.new_item',
                           name='ticket_new'),
                       )

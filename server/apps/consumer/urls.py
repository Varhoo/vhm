
from django.conf.urls.defaults import *

urlpatterns = patterns(
    'apps.consumer.views',
    (r'^$', 'startOpenID'),
    (r'^finish/$', 'finishOpenID'),
#    (r'^xrds/$', 'rpXRDS'),
)

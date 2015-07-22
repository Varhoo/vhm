from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.core.models import Server


class Record(models.Model):
    server = models.ForeignKey(Server)
    datecreated = models.DateTimeField(_('Dateime'), default=datetime.now)
    name = models.CharField(max_length=64)
    value = models.FloatField()

    def __unicode__(self):
        return "%s [%s]" % (self.name, self.server)

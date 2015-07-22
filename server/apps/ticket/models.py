from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
import settings

ENUM_STATUS = (
    (1, "NEW"),
  (2, "PROGRESS"),
  (3, "CLOSED"),
  (4, "DUPLICATED"),
)

ENUM_PRIORITY = (
    (1, "Low"),
  (2, "Medium"),
  (3, "High"),
)


class Group(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    users = models.ManyToManyField(User)

    def __unicode__(self):
        return self.name


class Ticket(models.Model):
    title = models.CharField(max_length=256)
    text = models.TextField()
    pub_date = models.DateTimeField(
        _('pub date'), default=datetime.now, editable=False)
    status = models.IntegerField(
        choices=ENUM_STATUS, default=1, blank=True, null=True)
    priority = models.IntegerField(choices=ENUM_PRIORITY, default=1)
    owner = models.ForeignKey(
        User, related_name="Owner", blank=True, null=True)
    author = models.ForeignKey(User, verbose_name="User")
    group = models.ForeignKey('Group', verbose_name='Groups', default=1)

    def __unicode__(self):
        return self.title  # + " " + self.pub_date

    def enum_priority(self):
        return [it[1] for it in ENUM_PRIORITY if it[0] == self.priority][0]

    def enum_status(self):
        return [it[1] for it in ENUM_STATUS if it[0] == self.status][0]

    @models.permalink
    def get_absolute_url(self):
        return ("ticket_id", [self.id])


class Comment(models.Model):
    pub_date = models.DateTimeField(
        _('pub date'), default=datetime.now, editable=False)
    author = models.ForeignKey(User)
    text = models.TextField()
    ticket = models.ForeignKey('Ticket', verbose_name='Tickets')
    is_public = models.BooleanField(default=True)
    upload_file = models.FileField(upload_to="upload/", blank=True, null=True)
    info_type = models.IntegerField('Type', default=1)

    def __unicode__(self):
        return self.text

    def get_file_url(self):
        if self.upload_file:
            return settings.MEDIA_URL + ("%s" % self.upload_file)

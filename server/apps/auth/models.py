import base64
from hashlib import sha1

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save


def create_htpasswd(raw_password):
    h = sha1()
    h.update(raw_password)
    return "{SHA}%s" % base64.b64encode(h.digest())

# Create your models here.


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    hash_pass = models.CharField(
        "hash password", max_length=128, blank=True, null=True)
    openid = models.CharField("openid", max_length=128, blank=True, null=True)

    def __unicode__(self):
        return "%s %d " % (self.user, self.id)

    def save(self, *args, **kwargs):
        if not self.pk:
            try:
                p = UserProfile.objects.get(user=self.user)
                self.pk = p.pk
                self.hash_pass = p.hash_pass
            except UserProfile.DoesNotExist:
                pass

        super(UserProfile, self).save(*args, **kwargs)


old_set_password = User.set_password


def set_password(user, raw_password):
    user.hash_pass = raw_password
    old_set_password(user, raw_password)

User.set_password = set_password


def create_user_profile(sender, instance, created, **kwargs):
    """Create the UserProfile when a new User is saved"""
    if created:
        profile = UserProfile.objects.get_or_create(user=instance)[0]
        profile.hash_pass = create_htpasswd(instance.hash_pass)
        profile.save()
    else:
    # update password
        try:
            up = UserProfile.objects.get(user=instance.id)
            up.hash_pass = create_htpasswd(instance.hash_pass)
            up.save()
        except AttributeError:
            pass

post_save.connect(create_user_profile, sender=User)


from django.db.models.signals import pre_delete, post_save
from django.dispatch.dispatcher import receiver
from apps.apftpmy.models import Account, ProjectSetting
from apps.xmlrpc.models import ActionServer

@receiver(pre_delete, sender=Account)
def account_delete(sender, instance, **kwargs):
    print "deleting %s" % instance

@receiver(post_save, sender=Account)
def account_save(sender, instance, **kwargs):
    if kwargs["created"]:
        a = ActionServer(command="user create %s %s" % (instance.user, instance.path), command_type=100, server=instance.server)
        a.save()
    else:
       pass 


@receiver(post_save, sender=ProjectSetting)
def project_save(sender, instance, **kwargs):
    if kwargs["created"]:
        a = ActionServer(command="user project %s %s" % (instance.user, instance.path), command_type=100, server=instance.server)
        a.save()
    else:
       pass 

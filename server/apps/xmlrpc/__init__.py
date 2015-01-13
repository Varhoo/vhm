
from django.db.models.signals import pre_delete, post_save
from django.dispatch.dispatcher import receiver
from apps.core.models import Account, ProjectSetting, ProjectProc
from apps.xmlrpc.models import ActionServer

@receiver(pre_delete, sender=Account)
def account_delete(sender, instance, **kwargs):
    print "deleting %s" % instance

@receiver(post_save, sender=Account)
def account_save(sender, instance, **kwargs):
    if kwargs["created"]:
        a = ActionServer(command="user create %s %s" % (instance.user, instance.path),\
                         command_type=100,\
                         server=instance.server)
        a.save()
    else:
       pass 

@receiver(post_save, sender=ProjectSetting)
def project_save(sender, instance, **kwargs):
    a = ActionServer(command="project update %s" % (instance.id),\
                     command_type=100,\
                     server=instance.account.server)
    a.save()

@receiver(post_save, sender=ProjectProc)
def project_save(sender, instance, **kwargs):
    a = ActionServer(command="project update %s" % (instance.project.id),\
                     command_type=100,\
                     server=instance.project.account.server)
    a.save()

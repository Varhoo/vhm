
import logging

from django.dispatch.dispatcher import receiver

from apps.core.models import Account, ProjectProc, ProjectSetting
from apps.core.signals import (vhm_account_update, vhm_process_update,
                               vhm_project_update)
from apps.xmlrpc.models import ActionServer

log = logging.getLogger(__name__)


#@receiver(pre_delete, sender=Account)
# def account_delete(sender, instance, **kwargs):
#    print "deleting %s" % instance


def call(sender, action, instance, **kwargs):
    name = sender.__name__
    if not instance:
        log.warning("action %s is not created - missing instance" %s str(name))
        return
    command = "%s::%s::%s" % (str(name), action, int(instance.id))

    server = {
        ProjectProc: lambda: instance.project.account.server,
        ProjectSetting: lambda: instance.account.server,
        Account: lambda: instance.server
    }[type(instance)]()

    action = ActionServer(command=command,
                          command_type=100,
                          server=server)
    log.info("Push to queue: %s" % command)
    action.save()


# Account ProjectSetting
@receiver(vhm_project_update, sender=ProjectSetting)
def project_settings_save(sender, instance, **kwargs):
    call(sender, "update", instance, **kwargs)


# Account ProjectProc
@receiver(vhm_process_update, sender=ProjectProc)
def project__proc_save(sender, instance, **kwargs):
    call(sender, "update", instance, **kwargs)


# Account signals
@receiver(vhm_account_update, sender=Account)
def account_save(sender, instance, **kwargs):
    if kwargs["created"]:
        call(sender, "create", instance, **kwargs)
    else:
        call(sender, "update", instance, **kwargs)

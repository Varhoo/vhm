from django.core.management.base import BaseCommand, CommandError
from apps.svn_dav.models import *
from apps.auth.models import *
    
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = ('Generate svn rights for svn dav')
    requires_model_validation = True
    can_import_settings = True

    def handle(self, *args, **kwargs):
        init(*args, **kwargs)

ENUM_RIGHT = {1:"r",2:"rw"}

def init(*args, **kwargs):
    
    #if repository exist, create .. print SvnRepository.objects.all()
    if len(args) > 1:
        print "Only one parametr"
        return False

    if "rights" in args:
    # render svn rights 
        for it in SvnRepository.objects.all():
            tpm_path = ""
            for right in SvnUserRights.objects.filter(repository=it.id).order_by("path"):
                if tpm_path == right.path:
                    print "%s = rw" % right.user
                else:
                    print "\n[%s:%s]" % (it.name,right.path)
                    print "%s = %s" % (right.user, ENUM_RIGHT[right.rights])
                    tpm_path = right.path

    if "password" in args:
        # render users and passwords
        users_id =  SvnUserRights.objects.values_list("user").distinct()
        for it in UserProfile.objects.filter(user__in=[it[0] for it in users_id]):
            print "%s:%s" % (it.user.username, it.hash_pass)

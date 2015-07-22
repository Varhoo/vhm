from django.core.management.base import BaseCommand, CommandError

from apps.svn_dav.utils import Generate


class Command(BaseCommand):
    help = ('Generate svn rights for svn dav')
    requires_model_validation = True
    can_import_settings = True

    def handle(self, *args, **kwargs):
        init(*args, **kwargs)


def init(*args, **kwargs):

    # if repository exist, create .. print SvnRepository.objects.all()
    if len(args) > 1:
        print "Only one parametr"
        return False

    g = Generate()
    g.run()

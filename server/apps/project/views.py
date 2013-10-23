#from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from models import Project

@login_required
def index(request):
    projects = Project.objects.order_by("priority")
    return render_to_response('project-list.html',
            {'projects': projects},
            context_instance=RequestContext(request))

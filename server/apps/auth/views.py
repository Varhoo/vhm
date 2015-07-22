# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from models import *
import random


def create_profil_from_ipenid(request, result):
    profile = UserProfile.objects.filter(openid=result["openid"])
    if not profile:
        # user not exist
        # create and save user
# TODO
        # * generate password
        # * generate login
        username = "guest%d" % random.randrange(1, 10000, 1)
        user = User.objects.create_user(username, result["email"], 'pavel1987')
        user.first_name = result["first_name"]
        user.last_name = result["last_name"]
        user.is_activ = True
        user.is_staff = True
        user.save()
        # save profile
        profile = UserProfile.objects.get(user=user)
        profile.openid = result["openid"]
        profile.save()
        user.username = "quest%d" % user.id
        user.save()
    else:
        user = profile[0].user

    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
    return index(request)


def index(request):
    if request.method == 'POST':

        user = authenticate(username=request.POST[
                            "username"], password=request.POST["password"])
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect("/admin/")
            else:
                print "Your account has been disabled!"
        else:
            print "Your username and password were incorrect."

    template = "login.html"
    if request.user.is_authenticated():
        return HttpResponseRedirect("/admin/")

    return render_to_response(template,
                              {},
                              context_instance=RequestContext(request))

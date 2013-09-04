# -*- coding: utf-8 -*-
#Author: Pavel Studeník
#Email: studenik@varhoo.cz
#Date: 10.2.2010

from SimpleXMLRPCServer import SimpleXMLRPCDispatcher
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from apps.apftpmy.models import *
import settings
from django.db import models
from datetime import datetime, date
from django.utils.translation import ugettext_lazy as _

STATUS_ENUM = (
   (0, "Waiting"),
   (1, "In progress"),
   (2, "Done"),
   (3, "Error"),
)
#model for check
class Action(models.Model):
    account = models.ForeignKey(Account)
    last_modify = models.DateTimeField(_('Last Modify'),default=datetime.now)
    command = models.IntegerField();
    status = models.IntegerField(default=0);
 
class ActionServer(models.Model):
    server = models.ForeignKey(Server)
    last_modify = models.DateTimeField(_('Last Modify'),default=datetime.now)
    command = models.IntegerField();
    args = models.TextField(blank=True,null=True);
    status = models.IntegerField(default=0,choices=STATUS_ENUM);   
    exit_code = models.IntegerField(blank=True,null=True);   

dispatcher = SimpleXMLRPCDispatcher(allow_none=False, encoding=None)


@csrf_exempt
def rpc_handler(request):
        """
        the actual handler:
        if you setup your urls.py properly, all calls to the xml-rpc service
        should be routed through here.
        If post data is defined, it assumes it's XML-RPC and tries to process as such
        Empty post assumes you're viewing from a browser and tells you about the service.
        """

        if len(request.POST):
                response = HttpResponse(mimetype="application/xml")
                response.write(dispatcher._marshaled_dispatch(request.raw_post_data))
        else:
                response = HttpResponse()
                response.write("<h1>This is an XML-RPC Service.</h2>")
                response.write("<p>You need to invoke it using an XML-RPC Client!</p>")
                response.write("The following methods are available:<ul>")
                methods = dispatcher.system_listMethods()

                for method in methods:
                        sig = dispatcher.system_methodSignature(method)
                        # this just reads your docblock, so fill it in!
                        help =  dispatcher.system_methodHelp(method)

                        response.write("<li><b>%s</b>: [%s] %s" % (method, sig, help))
                response.write("</ul>")

        response['Content-length'] = str(len(response.content))
        return response

def check_auth(token):
        __token__ = settings.SECRET_KEY
        if token == __token__:
            return True
        else:
            return "error: bad auth"

def check_auth_host(token):
        try:
            srv = Server.objects.get(token=token)
            return srv
        except Server.DoesNotExist:
            return "error: bad auth"

def get_all_account(token):
        r = check_auth_host(token)
        if r == False:
            return r
        accounts = Account.objects.filter(server__token=token)
        return [{"id": it.id, "name": it.name, "path": it.path, "user": it.user} for it in accounts]

def get_all_repo(token):
        r = check_auth_host(token)
        if r == False:
            return r
        data = ApacheAlias.objects.filter(account__server__token=token, repo_type__gt=0, is_valid=True)
        return [{"id": it.id, "site": it.site, "path": it.account.path, 
                 "repo_version": it.repo_version, "repo_url": it.repo_url,
                 "repo_type": it.repo_type, "name": it.account.name, 
                 "user": it.account.user} for it in data]

def set_account_size(token,id,size):
        r = check_auth_host(token)
        if r == False:
            return r
        try:
            account = Account.objects.get(id=id,server__token=token)
            account.size=size
            account.save()
            return True
        except:
            return False

#only for main host
def set_domain_expirate(token,domain,expirate):
        r = check_auth(token)
        if r != True:
            return r
        try:
            dom = Domain.objects.get(name=domain)
            dom.expirate=datetime.date(datetime.strptime(expirate,"%Y-%m-%d"))
            dom.save()
            return True
        except Domain.DoesNotExist:
            return False

def set_account_uidguid(token,id,uid,gid):
        r = check_auth_host(token)
        if r == False:
            return r
        try:
            account = Account.objects.get(id=id,server__token=token)
            account.uid=uid
            account.gid=gid
            account.save()
            print account
            return True
        except Account.DoesNotExist:
            return False

# only for user
def action_for_project(token,action):
         acc = Account.objects.get(token=token)
         if len(Action.objects.filter(account=acc,command=action, status=0))>0:
            return "INFO: waiting, this action in sheduler"

         act = Action(account=acc,command=action)
         act.save()
         return True

def action_server_list(token):
        srv = check_auth_host(token)
        if srv == False:
            return srv
        actions = ActionServer.objects.filter(server__token=token, status=0)
        return [{"id": it.id, "command": it.command, "args": it.args, "srv": srv.os_type} for it in actions]

def action_server_status(token,id,status,exit_code=None):
        action = ActionServer.objects.get(server__token=token, id=id,status__in=(0,1))
        action.status = status
        action.exit_code = exit_code
        action.last_modify = datetime.now()
        action.save()
        return True

# you have to manually register all functions that are xml-rpc-able with the dispatcher
# the dispatcher then maps the args down.
# The first argument is the actual method, the second is what to call it from the XML-RPC side...
dispatcher.register_function(get_all_account, 'get_all_account')
dispatcher.register_function(set_account_size, 'set_account_size')
#function get all data of account with repository
dispatcher.register_function(get_all_repo, 'get_all_repo')
dispatcher.register_function(action_for_project, 'action_for_project')
dispatcher.register_function(set_account_uidguid, 'set_account_uidguid')
dispatcher.register_function(set_domain_expirate, 'set_domain_expirate')
dispatcher.register_function(action_server_list, 'action_server_list')
dispatcher.register_function(action_server_status, 'action_server_status')

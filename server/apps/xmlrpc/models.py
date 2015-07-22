#!/usr/bin/python
# coding: utf-8
# Author: Pavel Studeník
# Email: studenik@varhoo.cz
# Date: 10.2.2010

from datetime import date, datetime
from SimpleXMLRPCServer import SimpleXMLRPCDispatcher

from django.conf import settings
from django.db import models
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from apps.core.models import *
from apps.monitoring.models import *

STATUS_ENUM = (
    (0, "Waiting"),
   (1, "In progress"),
   (2, "Done"),
   (3, "Error"),
)


class Action(models.Model):
    account = models.ForeignKey(Account)
    last_modify = models.DateTimeField(_('Last Modify'), default=datetime.now)
    command = models.IntegerField()
    status = models.IntegerField(default=0)


class ActionServer(models.Model):
    server = models.ForeignKey(Server)
    status = models.IntegerField(default=0, choices=STATUS_ENUM)
    command = models.TextField(blank=True, null=True)
    command_type = models.IntegerField(default=0)
    role = models.CharField(max_length=64, default="root")
    result = models.TextField(blank=True)
    exit_code = models.IntegerField(blank=True, null=True)
    last_modify = models.DateTimeField(_('Last Modify'), default=datetime.now)


class SXD(SimpleXMLRPCDispatcher):

    def __init__(self, allow_none=False, encoding=None, ip=None):
        self.funcs = {}
        self.instance = None
        self.allow_none = allow_none
        self.encoding = encoding
        self.ip = ip

    # def _dispatch(self, method, params):
    #    print method, params
    #    res = super(SimpleXMLRPCDispatcher, self)._dispatch(method, params)
    #    print res

dispatcher = SXD(allow_none=True, encoding="utf8", )
# FIXME - exists better way to save global ip from requirement
ip = ""


@csrf_exempt
def rpc_handler(request):
    global ip
    """
        the actual handler:
        if you setup your urls.py properly, all calls to the xml-rpc service
        should be routed through here.
        If post data is defined, it assumes it's XML-RPC and tries to process as such
        Empty post assumes you're viewing from a browser and tells you about the service.
        """
    if len(request.body):
        ip = request.META["REMOTE_ADDR"]
        response = HttpResponse(mimetype="application/xml")
        data = dispatcher._marshaled_dispatch(request.body)
        response.write(data)

        #d = Xmlrpc(request)
    else:
        response = HttpResponse()
        response.write("<h1>This is an XML-RPC Service.</h2>")
        response.write("<p>You need to invoke it using an XML-RPC Client!</p>")
        response.write("The following methods are available:<ul>")
        methods = dispatcher.system_listMethods()

        for method in methods:
            sig = dispatcher.system_methodSignature(method)
            # this just reads your docblock, so fill it in!
            help = dispatcher.system_methodHelp(method)

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
        return None


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
    data = ProjectSetting.objects.filter(
        account__server__token=token, repo_type__gt=0, is_enabled=True)
    return [{"id": it.id, "site": it.site,
             "path": os.path.abspath("%s/%s" % (it.account.path, it.path)),
             "repo_version": it.repo_version, "repo_url": it.repo_url,
             "repo_type": it.repo_type, "name": it.account.name,
             "user": it.account.user} for it in data]


def get_all_projects(token):
    r = check_auth_host(token)
    if r == False:
        return r
    accounts = ProjectSetting.objects.filter(
        account__server__token=token, is_enabled=True)
    data = []
    for it in accounts:
        prj = ProjectProc.objects.filter(project=it)
        for it in prj:
            d = it.get_data()
            data.append(d)
    return data


def set_account_size(token, id, size):
    r = check_auth_host(token)
    if r == False:
        return r
    try:
        account = Account.objects.get(id=id, server__token=token)
        account.size = size
        account.save()
        return True
    except:
        return False


def get_server(token):
    r = check_auth_host(token)
    return r.__dict__


def get_projectproc(token, id):
    r = check_auth_host(token)
    if r == None:
        return r

    proj = Project.objects.get(id=id)
    # render data for apache configure
    # every project has alone file with more process
    procs = ProjectProc.objects.filter(
        project__id=id, project__account__server=r, template__file_type=MODE_ENUM_APACHE)
    key = proj.account.name

    data = {key: {
        "%s" % MODE_ENUM_APACHE: [],
        "%s" % MODE_ENUM_VHM: []
    },
    }
    for it in procs:
        filetype = it.template.file_type
        content = it.get_raw()
        data[key]["%s" % MODE_ENUM_APACHE].append(["%s" % content, ])

    # render data for uwsgi - all projects in one configure file
    procs = ProjectProc.objects.filter(
        project__id=id, project__account__server=r, template__file_type=MODE_ENUM_VHM)
    if len(procs) > 0:
        procs = ProjectProc.objects.filter(
            project__account__server=r, template__file_type=MODE_ENUM_VHM)
        for it in procs:
            content = it.get_raw()
            data[key]["%s" % MODE_ENUM_VHM].append(["%s" % content, ])
    return data

# only for main host


def set_domain_expirate(token, domain, expirate):
    r = check_auth(token)
    if r != True:
        return r
    try:
        dom = Domain.objects.get(name=domain)
        dom.expirate = datetime.date(datetime.strptime(expirate, "%Y-%m-%d"))
        dom.save()
        return True
    except Domain.DoesNotExist:
        return False


def set_account_uidguid(token, user, uid, gid):
    r = check_auth_host(token)
    if r == False:
        return r
    try:
        account = Account.objects.get(user=user, server__token=token)
        account.uid = uid
        account.gid = gid
        account.save()
        return True
    except Account.DoesNotExist:
        return False


def set_procs_running(token, data):
    r = check_auth_host(token)
    if r == None:
        return r

    for key, value in data.items():
        proc = ProjectProc.objects.get(id=int(key), project__account__server=r)
        proc.is_running = value
        proc.save()


# only for user
def action_for_project(token, action):
    acc = Account.objects.get(token=token)
    if len(Action.objects.filter(account=acc, command=action, status=0)) > 0:
        return "INFO: waiting, this action in sheduler"

    act = Action(account=acc, command=action)
    act.save()
    return True


def action_server_list(token):
    srv = check_auth_host(token)
    if srv == False:
        return srv
    actions = ActionServer.objects.filter(server__token=token, status=0)
    return [
        {"id": it.id, "command": it.command, "command_type": it.command_type,
         "role": it.role, "srv": srv.os_type} for it in actions]


def action_server_status(token, id, status, result="", exit_code=None):
    action = ActionServer.objects.get(
        server__token=token, id=id, status__in=(0, 1))
    action.status = status
    action.result = result
    action.exit_code = exit_code
    action.last_modify = datetime.now()
    action.save()
    return True


def ping(token):
    global ip
    srv = check_auth_host(token)
    if not srv:
        return False
    srv.last_checked = datetime.now()
    srv.global_ip = ip
    srv.save()
    return True


def set_monitoring_data(token, data):
    server = Server.objects.get(token=token)
    for it in data:
        r = Record(server=server, name=it, value=data[it])
        r.save()

# you have to manually register all functions that are xml-rpc-able with the dispatcher
# the dispatcher then maps the args down.
# The first argument is the actual method, the second is what to call it
# from the XML-RPC side...
dispatcher.register_function(get_all_account, 'get_all_account')
dispatcher.register_function(get_all_projects, 'get_all_projects')
dispatcher.register_function(set_account_size, 'set_account_size')
# function get all data of account with repository
dispatcher.register_function(get_all_repo, 'get_all_repo')
dispatcher.register_function(get_projectproc, 'get_projectproc')
dispatcher.register_function(get_server, 'get_server')
dispatcher.register_function(action_for_project, 'action_for_project')
dispatcher.register_function(set_account_uidguid, 'set_account_uidguid')
dispatcher.register_function(set_domain_expirate, 'set_domain_expirate')
dispatcher.register_function(set_procs_running, 'set_procs_running')
dispatcher.register_function(action_server_list, 'action_server_list')
dispatcher.register_function(action_server_status, 'action_server_status')
dispatcher.register_function(ping, 'ping')
# monitoring
dispatcher.register_function(set_monitoring_data, 'set_monitoring_data')

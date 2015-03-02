#!/usr/bin/python
# coding: utf-8
# Author: Pavel Studeník
# Email: studenik@varhoo.cz
# Date: 10.2.2010


import sys
import os
import re
import xmlrpclib
import commands
import subprocess
import utils
import logging
import psutil
import requests
import errno
from user import User
from socket import error as socket_error
from repository import *
from manager import manager

ENABLE_UWSGI_TAG = ['processes', 'chdir', 'uid', 'gid', 'pythonpath',
                    'limit-as', 'optimize', 'daemonize', 'master', 'home', 'no-orphans',
                    'pidfile', "wsgi-file", "socket"]

ROOT_HTTPD = {
    0: "/etc/apache2/sites-enabled/",  # site enable for debian
    1: "/etc/httpd/conf.d/"  # site enable for fedora
}


def getFolderSize(folder):
    total_size = os.path.getsize(folder)
    for item in os.listdir(folder):
        itempath = os.path.join(folder, item)
        if os.path.isfile(itempath):
            total_size += os.path.getsize(itempath)
        elif os.path.isdir(itempath):
            total_size += getFolderSize(itempath)
    return total_size


def aray2xml(data):
    def tag(tag, value):
        return "      <%s>%s</%s>" % (tag, value, tag)

    content = ["<server>"]
    for proc in data:
        content.append("   <uwsgi id=\"%d\">" % proc["id"])
        for key, it in proc.iteritems():
            if not key in ENABLE_UWSGI_TAG:
                continue
            if isinstance(it, bool):
                content.append("      <%s/>" % key)
            else:
                content.append(tag(key, it))
        content.append("   </uwsgi>")
    content.append("</server>")
    return "\n".join(content)


class ServerApp:

    def __init__(self, conf):
        protocol = "http" if not conf.ssl else "https"
        self.url = "%s://%s/xmlrpc/" % (protocol, conf.server)
        self.rpc_srv = xmlrpclib.ServerProxy(self.url, verbose=conf.verbose)
        self.conf = conf

        logging.basicConfig(level=conf.debuglevel)
        self.log = logging

    def login(self, token):
        self.token = token
        try:
            ping = self.rpc_srv.ping(self.token)
        except socket_error:
            self.log.error("it's not possible to connect %s" % self.url)
            return False

        if not ping:
            print "INFO: token does not exist"
            return False
        if self.conf.verbose > 0:
            print self.conf.server, ping

        return True

    def check_rights(self):
        result = self.rpc_srv.get_all_account(self.token)
        for it in result:
            subprocess.call(
                ['chown', '%s:%s' % (it["user"], self.conf.group), '-R', it["path"]])

    def check_size_all(self):
        """
        Get size of homedir and update data on the server
        """
        result = self.rpc_srv.get_all_account(self.token)
        for it in result:
            size = getFolderSize(it["path"])
            result = self.rpc_srv.set_account_size(
                self.token, it["id"], str(size / 10 ** 3))

    def check_services(self):
        mng = manager(self.conf)
        self.rpc_srv.set_procs_running(self.token, mng.get_list())

    def check_userid_all(self):
        result = self.rpc_srv.get_all_account(self.token)
        # for it in result:
        for it in result:
            try:
                u = User(it["user"])
            except TypeError:
                return False
            self.log.debug("uid=%s gid=%s" % (u.uid, u.gid))
            self.rpc_srv.set_account_uidguid(
                self.token,
                u.username,
                u.uid,
                u.gid)

    def get_all_account(self):
        result = self.rpc_srv.get_all_repo(self.token)
        return result

    def check_repo_all(self):
        result = self.rpc_srv.get_all_repo(self.token)

        for it in result:
            path, repo_id = it["path"], it["repo_type"]

            if not os.path.exists(path):
                self.log.error("path %s not exists" % path)
            else:
                self.log.debug("%d: (%s)" % (repo_id, path))

                if repo_id == 1:  # SVN
                    res = update_repo_svn(it)
                elif repo_id == 2:  # GIT
                    res = update_repo_git(it)

    def apache_restart(self):
        # restart apache service
        command = "service apache2 reload"
        self.log.info("command: %s" % command)
        result = commands.getstatusoutput(command)
        if result[0] > 0:
            print result[1]

    def apache_reload(self):
        # restart apache service
        command = "service apache2 reload"
        self.log.info("command: %s" % command)
        result = commands.getstatusoutput(command)
        if result[0] > 0:
            print result[1]

    def monitoring(self):
        if hasattr(psutil, "virtual_memory"):
                # rename from version 0.5.0
            mem = psutil.virtual_memory()
        else:
            mem = psutil.phymem_usage()
        cpu = psutil.cpu_percent(interval=1.)

        data = {
            "mem_free": mem.free,
            "mem_percent": mem.percent,
            "cpu_percent": cpu
        }
        self.rpc_srv.set_monitoring_data(self.token, data)

    def get_all_projects(self):
        result = self.rpc_srv.get_all_projects(self.token)
        return result

    def write_uwsgi(self, conf):
        data = self.rpc_srv.get_all_projects(self.token)
        for it in data:
            if hasattr(conf, "group"):
                it["gid"] = conf.group
        content = aray2xml(data)
        with open(conf.uwsgifile, "w") as f:
            f.write(content)
            f.close()

    def get_projectproc(self, conf, proj_id):
        data = self.rpc_srv.get_projectproc(self.token, proj_id)
        server = self.rpc_srv.get_server(self.token)
        os_type = server["os_type"]

        for name, procs in data.items():
            for key, proc in procs.items():
            # apache2 configuration
                if key == "1":
                    content = "\n".join([item[0] for item in proc])
                    filename = "%s%03d-%s" % (
                        ROOT_HTTPD[os_type],
                        proj_id,
                        name)

                    with open(filename, "w") as f:
                        f.write(content)
                        self.log.info("write to file %s" % filename)
                        f.close()

                elif key == "2":
                    rows = [item[0] for item in proc]
                    # if is empty, no write to file
                    if rows:
                        # render apache_file
                        filename = conf.uwsgifile
                        content = "\n".join(rows)
                        with open(filename, "w") as f:
                            f.write("<vhm>\n%s\n</vhm>" % content)
                            self.log.info("write to file %s" % filename)
                            f.close()
        return 0

    def do_all_actions(self, conf):
        data = self.rpc_srv.action_server_list(self.token)
        result = None
        # FIXME
        for it in data:

            self.rpc_srv.action_server_status(self.token, it["id"], 1)
            if int(it["command_type"]) == 100:
                d = it["command"].split("::")

                # check project
                if d[0] == "proc":
                    if d[1] in ["create", "update"]:
                        status = self.get_projectproc(conf, int(d[2]))
                        result = ""

                # update repository
                if d[0] == "repository":
                    if d[1] in ["update"]:
                        if d[2] in ["all"]:
                            self.check_repo_all()

                # check projects ##
                if d[0] == "project":
                    if d[1] in ["create", "update"]:
                        status = self.get_projectproc(conf, int(d[2]))
                        result = ""

                # check users ##
                if d[0] == "user":
                    u = User(d[2])
                    if d[1] == "create":
                        u.create(conf.group, d[3])
                    self.rpc_srv.set_account_uidguid(
                        self.token, u.username, u.uid, u.gid)
                    status = 0
                    result = "%s %s %s" % (u.username, u.uid, u.gid)

            else:
                if os.geteuid() == 0:
                    cmd = "su %s -c '%s'" % (it["role"], it["command"])
                else:
                    cmd = "%s" % (it["command"])
                status, result = commands.getstatusoutput(cmd)

            if status == 0:
                result = self.rpc_srv.action_server_status(
                    self.token, it["id"], 2, result, status)
            else:
                result = self.rpc_srv.action_server_status(
                    self.token, it["id"], 3, result, status)

    def __action_update(self, args, srv):
        def deb(args):
            print "UPDATE debian:"
            command = "apt-get update; apt-get upgrade -y"
            data = commands.getstatusoutput(command)
            return data

        def rpm(args):
            print "UPDATE fedora:"
            command = "yum update"
            data = commands.getstatusoutput(command)
            return data
        res = {
            0: lambda x: deb(x),
           1: lambda x: rpm(x),
        }[srv](args)

        print "result:", res[0]
        print "result:", res[1]
        return res[0]

    def send_file(self, filepath):
        r = requests.post(self.url, files={filepath: open(filepath, 'rb')})
        # need use better  way to upload file
        #self.rpc_srv.send_file( self.token, data)


class MainServerApp:

    def __init__(self, host):
        self.rpc_srv = xmlrpclib.ServerProxy("http://%s/xmlrpc/" % host)
        self.token = ''

    def check_demain_name(self, domain):
        expr = utils.get_dns_expire(domain)
        result = self.rpc_srv.set_domain_expi

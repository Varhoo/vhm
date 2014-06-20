#!/bin/python
# coding: utf-8
# author: Pavel Studenik
# email: studenik@varhoo.cz
# date: 5.10.2012

import sys, os, commands, re
#parse python file
import compiler 
import ConfigParser

# dynamic path for importing
ROOT_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), ".")

from vhmlib.vhmserver import *
from vhmlib.vhmcli import *

ENABLE_UWSGI_TAG = ['processes', 'chdir', 'uid', 'gid', 'pythonpath', 
        'limit-as', 'optimize', 'daemonize', 'master', 'home', 'no-orphans', 
        'pidfile', "wsgi-file"]


def aray2xml(data):
    def tag(tag, value):
        return "      <%s>%s</%s>" % (tag, value, tag)

    content = ["<server>"]
    for proc in data:
        content.append("   <uwsgi id=\"%d\">" % proc["id"])
        for key, it in proc.iteritems():
            if not key in ENABLE_UWSGI_TAG: continue
            if type(it) == bool:
                content.append("      <%s/>" % key)
            else:
                content.append(tag(key, it))
        content.append("   </uwsgi>")
    content.append("</server>")
    return "\n".join(content)


class Config:
    def __init__(self):
        path = "/etc/vhm.conf"

        config = ConfigParser.ConfigParser()
        if not os.path.exists(path):
            try:
                self.create(path)
            except IOError:
                path = os.path.expanduser('~/.vhm.conf')
                if not os.path.exists(path):
                    self.create(path)
        config.read(path)
        self.conf = config

        self.token = self.get("client", "token")
        self.server = self.get("client", "server")
        self.verbose = self.getint("client", "verbose")
        self.monitoring = self.getboolean("client", "monitoring", default=False)
        self.webproject = self.getboolean("client", "webproject", default=False)
        self.ssl = self.getboolean("client", "ssl_enable", default=False)
        self.group = self.get("webproject", "group")
        self.smtp = self.get("smtp", "host", default=False)

    def create(self, path):
        config = ConfigParser.ConfigParser()
        config.add_section("client")
        config.add_section("webproject")
        config.add_section("smtp")
        config.set("client", "token", "")
        config.set("client", "server", "")
        config.set("client", "verbose", "0")
        config.set("client", "ssl_enable", "False")
        config.set("webproject", "group", "webuser")
        config.write(open(path, 'w'))

    def getboolean(self, sec, name, default=None):
        if self.conf.has_option(sec, name):
            return self.conf.getboolean(sec, name)
        else:
            return default

    def getint(self, sec, name, default=None):
        if self.conf.has_option(sec, name):
            return self.conf.getint(sec, name)
        else:
            return default

    def get(self, sec, name, default=None):
        if self.conf.has_option(sec, name):
            return self.conf.get(sec, name)
        else:
            return default
        
 
if __name__ == "__main__":
    # config file
    conf = Config()    
 
    srv = ServerApp(conf)
    srv.login(conf.token)

    # pick up and run events

    """ Run all script for this systems. """
    srv.do_all_actions(conf)

    """ send data for monitoring """
    if conf.monitoring:
        srv.monitoring()
   
    """ create repo for web project - apache2/uwsgi"""
    if conf.webproject: 
        data =  srv.get_all_projects()
        content = aray2xml(data)

        """ Check all repository on this system. """
        srv.check_repo()

        """ Recount size of full disk in all project on this system. """
        srv.check_size_all()





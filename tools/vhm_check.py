#!/bin/python
# coding: utf-8
# author: Pavel Studenik
# email: studenik@varhoo.cz
# date: 5.10.2012

import sys, os, commands, re
#parse python file
import compiler 

# dynamic path for importing
ROOT_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), ".")

from vhmlib.vhmserver import *
from vhmlib.vhmcli import *
from vhmlib.config import Config

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

 
if __name__ == "__main__":
    # config file
    conf = Config()    
 
    srv = ServerApp(conf)
    status = srv.login(conf.token)

    if not status:
        sys.exit(100)

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





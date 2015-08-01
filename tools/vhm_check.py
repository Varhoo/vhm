#!/bin/python
# coding: utf-8
# author: Pavel Studenik
# email: studenik@varhoo.cz
# date: 5.10.2012

import commands
import compiler
import logging
import os
import re
import sys

from vhmlib.config import Config
from vhmlib.manager import manager
from vhmlib.vhmcli import *
from vhmlib.vhmserver import *

# dynamic path for importing
ROOT_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), ".")


def main():
    # config file
    conf = Config()
    actions = []

    debuglevel = logging.ERROR
    for it in sys.argv[1:]:
        if it == ("-v"):
            debuglevel = logging.WARNING
        elif it == ("-vv"):
            debuglevel = logging.INFO
        elif it == ("-vvv"):
            debuglevel = logging.DEBUG
        if it == ("--valid"):
            actions.append("valid")

    conf.debuglevel = debuglevel

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
        #data =  srv.get_all_projects()
        #content = aray2xml(data)

        """ Check all repository on this system. """
        srv.check_repo_all()

        """ Recount size of full disk in all project on this system. """
        srv.check_size_all()

        """ reset owners for projects """
        srv.check_rights()

        """ check running services """
        srv.check_services()

        mng = manager(conf)
        for it in actions:
            fc = getattr(mng, it)
            fc()

if __name__ == "__main__":
    main()

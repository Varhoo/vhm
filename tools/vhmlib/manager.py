#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) Adam Strauch
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#     1. Redistributions of source code must retain the above copyright notice,
#        this list of conditions and the following disclaimer.
#
#     2. Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in the
#        documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDER "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import errno
import grp
import logging
import os
import shlex
import sys
import time
from optparse import OptionParser
from pwd import getpwnam
from subprocess import PIPE, Popen, call
from xml.etree.ElementTree import XMLParser

UWSGIs_PATH = "/usr/local/bin/uwsgi"


class manager:
    config_tree = None
    config = {}

    def __init__(self, conf):
        f = open(conf.uwsgifile)
        logging.basicConfig(level=conf.debuglevel)
        self.log = logging
        xml_src = f.read()
        f.close()

        parser = XMLParser()
        parser.feed(xml_src)
        self.config_tree = parser.close()

        self.parse()

    def parse(self):
        for element in self.config_tree:
            web_id = int(element.get("id"))
            self.config[web_id] = {}
            for subelement in element:
                self.config[web_id][subelement.tag] = subelement.text

    #
    # Process manipulation
    #

    def run_cmd(self, cmd):
        return_code = call(shlex.split(cmd))

        if not return_code:
            return True
        else:
            print "Error: '%s' return %d" % (cmd, return_code)
            return False

    def send_signal(self, id, signal):
        if not os.path.isfile(self.config[id]["pidfile"]):
            return False
        try:
            os.kill(self.get_pid(id), signal)
            return True
        except OSError as err:
            if err.errno == errno.ESRCH:
                return False
            elif err.errno == errno.EPERM:
                print id
                print "No permission to signal this process!"
                sys.exit(1)
            else:
                print id
                print "Unknown error"
                sys.exit(1)
        else:
            return True

    def running_check(self, id):
        return self.send_signal(id, 0)

    def get_pid(self, id):
        f = open(self.config[id]["pidfile"])
        try:
            pid = int(f.read().strip())
        except ValueError:
            print "Wrong PID format (int %s)" % self.config[id]["pidfile"]
            sys.exit(1)
        f.close()
        return pid

    def check_id(self, id):
        if not id in self.config:
            print "ID not found"
            sys.exit(1)

    #{'43': {'wsgi-file': '/home/cx/co/sexflirt/sexflirt.wsgi', 'processes': '1', 'uid': 'cx', 'pythonpath': '/home/cx/co/', 'limit-as': '48', 'chmod-socket': '660', 'gid': 'cx', 'master': None, 'home': '/home/cx/virtualenvs/default', 'optimize': '1', 'socket': '/home/cx/uwsgi/sexflirt.cz.sock'}}

    # Actions it selfs

    def start(self, id):
        self.check_id(id)

        python_bin = self.config[id]["home"] + "/bin/python -V"
        p = Popen(shlex.split(python_bin), stdout=PIPE, stderr=PIPE)
        data_raw = p.communicate()
        version = ".".join(data_raw[1].split(" ")[1].split(".")[0:2])

        uwsgi_bin = "%s%s" % (UWSGIs_PATH, version.replace(".", ""))
        if not os.path.isfile(uwsgi_bin):
            uwsgi_bin = "/usr/bin/uwsgi"

        if not self.running_check(id):
            if os.getuid() == 0:
                cmd = "su %s -c '%s -x %s:%d'" % (
                    self.config[id]["uid"],
                    uwsgi_bin,
                    self.config_file,
                    id)
            else:
                cmd = "%s -x %s:%d" % (uwsgi_bin, self.config_file, id)
            self.run_cmd(cmd)

    def startall(self):
        for web in self.config:
            self.start(web)

    def stop(self, id):
        self.check_id(id)
        if self.running_check(id):
            if not self.send_signal(id, 3):  # QUIT signal
                print "Error QUIT"
            time.sleep(1)
            if self.running_check(id):
                if not self.send_signal(id, 9):  # KILL signal
                    print "Error KILL"
            time.sleep(1)
        else:
            print "Error: app %d doesn't run" % id

    def stopall(self):
        for web in self.config:
            self.stop(web)

    def restart(self, id):
        self.check_id(id)
        if self.running_check(id):
            self.stop(id)
        if not self.running_check(id):
            self.start(id)

    def restartall(self):
        for web in self.config:
            self.restart(web)

    def reload(self, id):
        self.check_id(id)
        if self.running_check(id):
            return self.send_signal(id, 1)
        else:
            self.start(id)

    def brutal_reload(self, id):
        self.check_id(id)
        if self.running_check(id):
            return self.send_signal(id, 15)
        else:
            self.start(id)

    def brutal_reloadall(self):
        for web in self.config:
            self.brutal_reload(web)

    def check(self, id):
        self.check_id(id)
        if self.running_check(id):
            print "Aplikace běží"
        else:
            print "Aplikace neběží"

    def list(self):
        for app in self.config:
            if os.getuid() != 0 and os.getlogin() != self.config[app]["uid"]:
                continue
            prefix = "run"
            if not self.running_check(app):
                prefix = "not"
            print "%s %d: %s (%s)" % (prefix, app, self.config[app]["wsgi-file"], self.config[app]["uid"])

    def get_list(self):
        data = {}
        for app in self.config:
            if os.getuid() != 0 and os.getlogin() != self.config[app]["uid"]:
                continue
            prefix = True
            if not self.running_check(app):
                prefix = False
            data["%s" % app] = prefix
        return data

    def valid(self):
        valid_dirs = ["chdir", "pythonpath"]
        valid_files = ["pidfile", "daemonize", "wsgi-file", ]

        def get_rights(path):
            try:
                f = os.stat(path)
            except OSError:
                return (None, None)
            uid = f.st_uid
            gid = f.st_gid
            return (uid, gid)

        for app in self.config:
            user = self.config[app]["uid"]
            uid = getpwnam(user).pw_uid
            gid = getpwnam(user).pw_gid
            guid = [
                g for g in grp.getgrall() if g.gr_name == self.config[app]["gid"]]

            if guid and guid[0].gr_gid != gid:
                self.log.error("%s:%s %s" % (uid, gid, guid[0].gr_gid))

            for key in self.config[app].keys():
                if key in valid_dirs:
                    filepath = self.config[app][key]
                elif key in valid_files:
                    filepath = self.config[app][key]
                else:
                    continue
                u, g = get_rights(filepath)
                if u != uid or g != gid:
                    self.log.error(
                        "%s: file %s %s:%s %s:%s" %
                        (key, filepath, u, g, uid, gid))

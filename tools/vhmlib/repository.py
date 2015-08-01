#!/bin/python
# coding: utf-8
# author: Pavel Studenik
# email: studenik@varhoo.cz
# date: 5.10.2012

import commands
import os
import smtplib
from email.mime.text import MIMEText


#from django.core.mail import send_mail


def get_admins_from_django(homedir):
    return ["root@localhost"]
    """ Get admin's emails from django settings """
    path = homedir + "/settings/basic.py"
    if not os.path.exists(path):
        path = homedir + "/settings.py"

    if not os.path.exists(path):
        return

    mod = compiler.parseFile(path)
    for node in mod.node.nodes:
        try:
            if node.asList()[0].name == "ADMINS":
                # print dir(node.asList()[1].nodes)
                # print node.asList()[1].nodes
                return [it.nodes[1].value for it in node.asList()[1].asList()]
        except:
            pass


def send_mail(subject, body, email_from, emails_to):
    """ Funxtion for sending email though gmail """
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = email_from
    msg['To'] = ", ".join(emails_to)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.ehlo()  # for tls add this line
    s.starttls()  # for tls add this line
    s.ehlo()  # for tls add this line
    s.login(SMTP_USERNAME, SMTP_PASSWORD)
    s.sendmail(email_from, emails_to, msg.as_string())
    s.quit()


def update_repo_svn(data):
    homedir = os.path.join(data["path"])

    # update count
    update_count = 0

    command_status = "cd %s; svn status" % homedir
    # FIXME - use better way for not empty string
    if len(data["repo_version"]) > 0:
        command_diff = "cd " + homedir + \
            "; svn diff -r BASE:%d" % int(data["repo_version"])
        command = "cd " + homedir + \
            "; svn update -r %d" % int(data["repo_version"])
    else:
        command_diff = "cd " + homedir + "; svn diff -r BASE:HEAD"
        command = "cd " + homedir + "; svn update"

    exitcode, result = commands.getstatusoutput(command_status)
    if result.startswith("svn: warning: W155007"):
        print "ERROR: svn does not exists"
        return

    result_diff = commands.getstatusoutput(command_diff)
    result = commands.getstatusoutput(command)

    # difference between version of svn
    if result[1].startswith("Updating"):
        tmp = result[1].split("\n")[1:]
        result_svn = "\n".join(tmp)
    else:
        result_svn = result[1]

    # exists some files for update
    if not result_svn.startswith("At revision"):
        update_count = update_count + 1

        emails = get_admins_from_django(homedir)
        # count files, which was updated
        count = len(result_svn.split("\n")) - 1

        # get last log (TODO show all last logs, not only last)
        command_log = "cd " + homedir + "; svn log -r COMMITTED"
        result_log = commands.getstatusoutput(command_log)

        command_chown = "chown %s:webusers %s/ -R" % (data["name"], homedir)
        result_chown = commands.getstatusoutput(command_chown)

        # create message
        subject = "VHM-SVN Update '%s' (%d files)" % (data["name"], count)
        msg = "Project '%s' on site '%s' was update (%d files)\n" % (
            data["name"], data["site"], count)
        msg += result_log[1]
        msg += "\n\n%s" % result_diff[1]
        msg += "\n\n-------------------------------\n"
        msg += "\n%s" % result[1]

        # send mail by python (no django)
        if emails:
            send_mail(subject, msg, "root@localhost", emails)

        # if exists some python files that apache service restart
        if len([it for it in result[1].split("\n") if it.endswith(".py")]) > 0:
            return 1
    return 0


def update_repo_git(data):
    homedir = os.path.join(data["path"])

    # update count
    update_count = 0

    # FIXME - use better way for not empty string
    if len(data["repo_version"]) > 0:
        command_diff = "cd " + homedir + \
            "; git diff -r BASE:%d" % int(data["repo_version"])
        command = "cd " + homedir + \
            "; git pull -r %d" % int(data["repo_version"])
    else:
        command_diff = "cd " + homedir + "; git diff -r BASE:HEAD"
        command = "cd " + homedir + "; git pull"

    result_diff = commands.getstatusoutput(command_diff)
    result = commands.getstatusoutput(command)

    if not result[1].startswith("Already up-to-date"):
        update_count = update_count + 1

        emails = get_admins_from_django(homedir)
        # count files, which was updated
        count = len(result[1].split("\n")) - 1

        # get last log (TODO show all last logs, not only last)
        command_log = "cd " + homedir + "; git log -n 1"
        result_log = commands.getstatusoutput(command_log)

        command_chown = "chown %s:webusers %s/ -R" % (data["name"], homedir)
        result_chown = commands.getstatusoutput(command_chown)

        subject = "VHM-GIT Update '%s' (%d files)" % (data["name"], count)
        msg = "Project '%s' on site '%s' was update (%d files)\n" % (
            data["name"], data["site"], count)
        msg += result_log[1]

        if emails:
            send_mail(subject, msg, SMTP_USERNAME, emails)

        # if exists some python files that apache service restart
        if len([it for it in result[1].split("\n") if it.endswith(".py")]) > 0:
            return 1
    return 0

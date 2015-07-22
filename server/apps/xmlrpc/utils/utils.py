#!/bin/python

import commands
import re
from datetime import *


def diff_date_days(d1, d2):
    return (int(d1.strftime("%s")) - int(d2.strftime("%s"))) / (3600 * 24)


def get_dns_expire(domain):

    command = "whois %s | grep expire" % domain
    date_exp = "%d.%m.%Y"
    string_exp = r"([.0-9]+)"
    # org have other date format
    if domain.endswith(".org") or domain.endswith(".info"):
        command = "whois %s | grep ^Expiration" % domain
        date_exp = "%d-%b-%Y"
        string_exp = r"Date:([^ ]*) "

    if domain.endswith(".com"):
        command = "whois %s | grep ^expires:" % domain
        date_exp = "%Y-%m-%d"
        string_exp = r" ([0-9-]+) "

    data = commands.getstatusoutput(command)
    if data[0] == 0:
        m = re.search(string_exp, data[1])
        if m:
            return datetime.date(datetime.strptime(m.group(1), date_exp))
    print command, data
    return None

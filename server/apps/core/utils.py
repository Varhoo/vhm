#!/bin/python

import commands
import re
from datetime import datetime
import socket
import logging

logger = logging.getLogger(__name__)


def dns_save_object(_object):
    old_expr = _object.expirate
    new_expr = get_dns_expire(_object.name)
    _object.last_modify = datetime.now()
    if old_expr != new_expr and new_expr != None:
        _object.expirate = new_expr
        logger.info("%s changed  %s -> %s" %
                    (_object, old_expr, _object.expirate))
    try:
        _object.ip_address = socket.gethostbyname(_object.name)
    except:
        _object.ip_address = socket.gethostbyname("www.%s" % _object.name)
    _object.save()


def diff_date_days(d1, d2):
    return (int(d1.strftime("%s")) - int(d2.strftime("%s"))) / (3600 * 24)


def get_dns_expire(domain):

    command = "whois %s | grep expire" % domain
    date_exp = "%d.%m.%Y"
    string_exp = r"([.0-9]+)"
    # org have other date format
    if domain.endswith(".org") or domain.endswith(".info"):
        command = "whois %s | grep Expiry" % domain
        date_exp = "%d-%b-%Y"
        string_exp = r"Date:([^ ]*) "

    if domain.endswith(".com"):
        command = "whois %s | grep 'Registration Expiration'" % domain
        date_exp = "%Y-%m-%d"
        string_exp = r" ([0-9-]+) "

    data = commands.getstatusoutput(command)
    if data[0] == 0:
        m = re.search(string_exp, data[1])
        if m:
            date_str = datetime.strptime(m.group(1), date_exp)
            if date_str:
                return datetime.date(date_str)
            logger.warning("%s: %s" % (date_exp, data[1]))
    logger.warning("%s: %s" % (command, data))
    return None

# test
if __name__ == "__main__":
    print get_dns_expire("varhoo.cz")
    print get_dns_expire("wallplus.org")
    print get_dns_expire("mariepetrakova.com")
    print get_dns_expire("styrax.info")

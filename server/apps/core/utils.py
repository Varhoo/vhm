#!/bin/python

import commands,re
from datetime import datetime
import socket

def dns_save_object(_object):
    old_expr = _object.expirate
    new_expr = get_dns_expire(_object.name)
    _object.last_modify = datetime.now()
    if old_expr != new_expr and new_expr != None:
        _object.expirate = new_expr
        print "%s changed  %s -> %s" % (_object, old_expr, _object.expirate)
    try:
        _object.ip_address = socket.gethostbyname(_object.name)
    except:
        _object.ip_address = socket.gethostbyname("www.%s" % _object.name)
    _object.save()

def diff_date_days(d1,d2):
    return (int(d1.strftime("%s")) - int(d2.strftime("%s")))/(3600*24)

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
            return datetime.date(datetime.strptime(m.group(1),date_exp))
    print command, data
    return None

#test
if __name__=="__main__":
    print get_dns_expire("varhoo.cz")
    print get_dns_expire("wallplus.org")
    print get_dns_expire("mariepetrakova.com")
    print get_dns_expire("styrax.info")
    



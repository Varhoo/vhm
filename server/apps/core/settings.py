# -*- coding: utf-8 -*-
# Django Apache IIS

from django.conf import settings

# root directory for web proejcts
APACHE_DIR_LOCATION = getattr(settings, "APACHE_DIR_LOCATION", '/var/www/')
# Boot - create new directory
# old value
APACHE_CREATE_DIR = getattr(settings, "APACHE_DIR_LOCATION", True)
APACHE_GROUP = getattr(settings, "APACHE_GROUP", "webuser")
APACHE_POWER = {1:[1,2], # slow - 1 proccess and 2 theaters
                2:[2,4], # medium - 2 proccess and 4 theaters
                3:[3,6] # hight - 3 proccess and 6 theaters
                } 

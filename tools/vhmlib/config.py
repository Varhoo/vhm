import ConfigParser
import os

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
        self.uwsgifile = self.get("webproject", "file", "/etc/uwsgi/config.xml")
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
        config.set("webproject", "file", "/etc/uwsgi/config.xml")
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
        

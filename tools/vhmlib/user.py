import commands
import os
import pwd
import sys


class User:

    def __init__(self, username):
        self.username = username
        self.check()

    def check(self):
        try:
            user = pwd.getpwnam(self.username)
            self.uid = user.pw_uid
            self.gid = user.pw_gid
            self.home = user.pw_dir
            self.is_exist = True
        except KeyError:
            self.is_exist = False
        return self.is_exist

    def exist(self):
        return self.is_exist

    def create(self, group, homedir):
        if self.exist():
            return

        if not os.path.exists(homedir):
            os.makedirs(homedir)

        command = "useradd -g %s -d %s %s" % (group, homedir, self.username)
        data = commands.getstatusoutput(command)
        if data[0] != 0:
            msg = "USER Error: Can't create user.\n"
            sys.stderr.write(msg)
            return False

        command = "chown %s:%s -R %s" % (self.username, group, homedir)
        data = commands.getstatusoutput(command)
        self.check()

    def delete(self):
        if self.exist():
            command = "userdel %s" % (self.username)
            data = commands.getstatusoutput(command)
            if data[0] != 0:
                msg = "USER Error: Can't create user.\n"
                sys.stderr.write(msg)
                return False
        self.check()
        return True

    def rename(self, newname):
        pass

if __name__ == "__main__":
    u = User("pavel")
    print u.__dict__

    u = User("pavel2")
    u.create("pavel", "/var/www/testing")
    u.delete()
    print u.__dict__

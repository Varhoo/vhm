import sys, os, re
import xmlrpclib, commands
import utils
from repository import *
import psutil
from user import User


def getFolderSize(folder):
    total_size = os.path.getsize(folder)
    for item in os.listdir(folder):
        itempath = os.path.join(folder, item)
        if os.path.isfile(itempath):
            total_size += os.path.getsize(itempath)
        elif os.path.isdir(itempath):
            total_size += getFolderSize(itempath)
    return total_size


class ServerApp:
   def __init__(self, conf):
      protocol = "http" if not conf.ssl else "https"
      url = "%s://%s/xmlrpc/?get=test" % (protocol, conf.server) 
      self.rpc_srv = xmlrpclib.ServerProxy(url, verbose=conf.verbose)
      self.conf = conf

   def login(self, token):
      self.token = token
      ping = self.rpc_srv.ping(self.token)
      if self.conf.verbose > 0:
	 print self.conf.server, ping

   def check_size_all(self):
      """
      Get size of homedir and update data on the server
      """
      result = self.rpc_srv.get_all_account( self.token  )
      for it in result:
         size = getFolderSize(it["path"])         
         result = self.rpc_srv.set_account_size( self.token, it["id"], size )

   def check_userid_all(self):
      result = self.rpc_srv.get_all_account( self.token  )
      #for it in result:
      for it in result:
         try:
            u = User(it["user"])
         except TypeError:
            return False
         print "debug: uid=%s gid=%s" % ( u.uid, u.gid )
         self.rpc_srv.set_account_uidguid(self.token, u.username, u.uid, u.gid)

   def get_all_account(self):
       result = self.rpc_srv.get_all_repo( self.token  )
       return result

   def check_repo(self):
       result = self.rpc_srv.get_all_repo( self.token  )

       for it in result:
          path, repo_id = it["path"], it["repo_type"]

          if not os.path.exists(path):
             print "path %s not exists" % path
          else:
             print path, repo_id

             if repo_id == 1: #SVN
                 res = update_repo_svn(it)
             elif repo_id == 2: #GIT
                 res = update_repo_git(it)
         
   def apache_restart(self):
        # restart apache service
        if count > 0:
            command = "service apache2 restart" 
            print "[ INFO ] \t Service apache restart ..."
            result = commands.getstatusoutput(command)
            if result[0] > 0:
                print result[1]

   def monitoring(self):
        if hasattr(psutil, "virtual_memory"):
            # rename from version 0.5.0
            mem = psutil.virtual_memory()
        else:
            mem = psutil.phymem_usage()
        cpu = psutil.cpu_percent(interval=1.)

        data = {
            "mem_free": mem.free,
            "mem_percent": mem.percent,
            "cpu_percent": cpu
        }
        self.rpc_srv.set_monitoring_data(self.token, data)

   def get_all_projects(self):
      result = self.rpc_srv.get_all_projects( self.token  )
      return result

   def do_all_actions(self, conf):
      data = self.rpc_srv.action_server_list( self.token  )
      #FIXME
      for it in data:
         result = self.rpc_srv.action_server_status( self.token, it["id"], 1  )
         if int(it["command_type"]) == 100:
            d = it["command"].split()
            print d
            if d[0] == "user":
                u = User(d[2])
                if d[1] == "create":
                    u.create(conf.group, d[3])
                self.rpc_srv.set_account_uidguid(self.token, u.username, u.uid, u.gid)
                status = 0
                resutl = "%s %s %s" % (u.username, u.uid, u.gid)
         else:
             if os.geteuid() == 0:
                 cmd =  "su %s -c '%s'" % (it["role"], it["command"])
             else:
                 cmd =  "%s" % (it["command"])
             status, result = commands.getstatusoutput(cmd)

         if status == 0:
            result = self.rpc_srv.action_server_status( self.token, it["id"], 2, result, status )
         else:
            result = self.rpc_srv.action_server_status( self.token, it["id"], 3, result, status )

   def __action_update(self,args,srv):
      def deb(args):
         print "UPDATE debian:"
         command = "apt-get update; apt-get upgrade -y"
         data = commands.getstatusoutput(command)
         return data

      def rpm(args):
         print "UPDATE fedora:"
         command = "yum update"
         data = commands.getstatusoutput(command)
         return data
      res = {
         0: lambda x: deb(x),
         1: lambda x: rpm(x),
      }[srv](args)

      print "result:", res[0]
      print "result:", res[1]
      return res[0] 


class MainServerApp:

   def __init__(self,host):
      self.rpc_srv = xmlrpclib.ServerProxy("http://%s/xmlrpc/" % host)
      self.token = ''

   def check_demain_name(self,domain):
      expr = utils.get_dns_expire(domain)
      result = self.rpc_srv.set_domain_expirate( self.token, domain, str(expr) )
      

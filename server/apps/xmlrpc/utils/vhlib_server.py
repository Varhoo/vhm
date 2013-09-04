import sys, os, re
import xmlrpclib, commands
import utils

def getFolderSize(folder):
    total_size = os.path.getsize(folder)
    for item in os.listdir(folder):
        itempath = os.path.join(folder, item)
        if os.path.isfile(itempath):
            total_size += os.path.getsize(itempath)
        elif os.path.isdir(itempath):
            total_size += getFolderSize(itempath)
    return total_size

def getUidGidByUser(user):
    #get information about user
    command = "id %s" % (user)
    data = commands.getstatusoutput(command)
    #check new user and get uid, gid
    if data[0] > 0:
        msg = "Error: User %s not found.\n" % user
        sys.stderr.write(msg) 
        return None
    else:
        m1 = re.search('uid=([0-9]*)', data[1])
        m2 = re.search('gid=([0-9]*)', data[1])
        uid = m1.group(1)  
        gid = m2.group(1)

    return (uid, gid)


class ServerApp:
   def __init__(self, host):
      self.rpc_srv = xmlrpclib.ServerProxy("http://%s/xmlrpc/" % host)
      self.token = ''

   def check_size_all(self):
      """
      Get size of homedir and update data on the server
      """
      result = self.rpc_srv.get_all_account( self.token  )
      print "debug: %s" % result
      for it in result:
         size = getFolderSize(it["path"])         
         result = self.rpc_srv.set_account_size( self.token ,it["id"],size )

   def check_userid_all(self):
      result = self.rpc_srv.get_all_account( self.token  )
      #for it in result:
      for it in result:
         try:
            uid, gid = getUidGidByUser(it["user"])
         except TypeError:
            return False
         print "debug: uid=%s gid=%s" % ( uid, gid )
         self.rpc_srv.set_account_uidguid(self.token, it["id"], uid, gid)

   def get_all_account(self):
       result = self.rpc_srv.get_all_repo( self.token  )
       return result

   def check_action_all(self):
      result = self.rpc_srv.action_server_list( self.token  )
      print "debug:", result
      for it in result:
         result = self.rpc_srv.action_server_status( self.token, it["id"], 1  )
         status = {
           1: lambda x,y: self.__action_update(x,y),
           2: lambda x,y: "action 2" + x ,
           3: lambda x,y: "action 3" + x 
         }[it["command"]](it["args"],it["srv"])
         if status == 0:
            result = self.rpc_srv.action_server_status( self.token, it["id"], 2, status )
         else:
            result = self.rpc_srv.action_server_status( self.token, it["id"], 3, status )

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

   def __init__(self, host):
      self.rpc_srv = xmlrpclib.ServerProxy("http://%s/xmlrpc/" % host)
      self.token = ''

   def check_demain_name(self,domain):
      expr = utils.get_dns_expire(domain)
      result = self.rpc_srv.set_domain_expirate( self.token, domain, str(expr) )
      

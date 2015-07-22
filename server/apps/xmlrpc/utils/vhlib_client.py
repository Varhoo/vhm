
import sys
import xmlrpclib


class App:

    def __init__(self, server, token):
        self.rpc_srv = xmlrpclib.ServerProxy("http://%s/xmlrpc/" % server)
        self.token = token

    def update_project(self):
        result = self.rpc_srv.action_for_project(self.token, 1)
        print result

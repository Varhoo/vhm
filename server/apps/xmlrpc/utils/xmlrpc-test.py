from vhlib_client import *
from vhlib_server import *

if __name__ == "__main__":
    #   app = App("localhost:8000","ahoj")
    #   app.update_project()
    srv = ServerApp("admin.varhoo.cz")
    srv = ServerApp("localhost:8000")
    print srv.get_all_account()
#    srv.check_size_all()
#    srv.check_userid_all()
#    srv.check_action_all()
#    srv.check_demain_name("varhoo.cz")

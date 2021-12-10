#!/usr/bin/python3
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import sys
import autodestroy
import time

if len(sys.argv) > 1:
    ADID = autodestroy.configure("30 minutes")
else:
    sys.stdout.write("Please enter password.\n")
    exit()


class Handler(FTPHandler):
    login_time = time.time()

    def on_login(self,username):
        Handler.login_time = int(time.time())

    def on_disconnect(self):
        if time.time() - Handler.login_time > 2.:
            exit()

authorizer = DummyAuthorizer()
authorizer.add_user("admin", sys.argv[1], "/home/minecraft/testsync/", perm="elradfmwMT")

handler = Handler
handler.authorizer = authorizer

server = FTPServer(("0.0.0.0", 21211), handler)
server.serve_forever()
autodestroy.cancel(ADID)
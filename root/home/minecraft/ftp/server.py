#!/usr/bin/python3
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import sys
import autodestroy
import time
import re
import os

if len(sys.argv) > 1:
    ADID = autodestroy.configure("30 minutes")
else:
    sys.stdout.write("Please enter password.\n")
    exit()


class Handler(FTPHandler):
    login_time = time.time()

    def on_file_received(self, file):
        dirname,filename = os.path.dirname(file),os.path.basename(file)
        normalfname = filename.replace("UNZIP_","")
        if re.search(r"^UNZIP_[\S\s]*?\.zip$",filename):
            os.system("mv {0}/{1} {0}/{2}".format(dirname,filename,normalfname))
            os.mkdir("{}/{}".format(dirname,re.sub(r"\.zip$","",normalfname)))
            os.system("unzip {0}/{1} -d {0}/{2}".format(dirname,normalfname,re.sub(r"\.zip$","",normalfname)))
            os.system("rm {0}/{1}".format(dirname,normalfname))

    def ftp_RNTO(self, path):
        result = super().ftp_RNTO(path)
        dirname,filename = os.path.dirname(path),os.path.basename(path)
        normalfname = re.sub(r"(UN)?ZIP_","",filename)
        if re.search(r"^UNZIP_[\S\s]*?\.zip$",filename):
            os.system("mv {0}/{1} {0}/{2}".format(dirname,filename,normalfname))
            os.mkdir("{}/{}".format(dirname,re.sub(r"\.zip$","",normalfname)))
            os.system("unzip {0}/{1} -d {0}/{2}".format(dirname,normalfname,re.sub(r"\.zip$","",normalfname)))
            os.system("rm {0}/{1}".format(dirname,normalfname))
        elif os.path.isdir(path) and re.search(r"^ZIP_",filename):
            os.system("mv {0}/{1} {0}/{2}".format(dirname,filename,normalfname))
            os.system("cd {0}/{1};zip -r ../{1}.zip ./*".format(dirname,normalfname))
            os.system("rm -r {0}/{1}".format(dirname,normalfname))
        return result

    def on_login(self,username):
        Handler.login_time = int(time.time())

    def on_disconnect(self):
        if time.time() - Handler.login_time > 2.:
            exit()

authorizer = DummyAuthorizer()
authorizer.add_user("admin", sys.argv[1], "/home/minecraft/palgservers/", perm="elradfmwMT")

handler = Handler
handler.authorizer = authorizer

server = FTPServer(("0.0.0.0", 21211), handler)
server.serve_forever()
autodestroy.cancel(ADID)
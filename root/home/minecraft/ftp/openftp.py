#!/usr/bin/python3
from subprocess import Popen, PIPE
import sys
import string
from random import choice

PATH = "/home/minecraft/ftp"

p = Popen(["screen","-ls"],stdout=PIPE,stderr=PIPE)
if ".ftp_server_screen" in p.communicate()[0].decode():
    sys.stdout.write("Server already running, sending password :\n\npassword = {}\n".format(open("{}/last_password.pass".format(PATH),"r").read()))
else:
    password = "".join([choice(string.ascii_letters + string.digits * 3) for i in range(32)])
    open("{}/last_password.pass".format(PATH),"w").write(password)
    p = Popen(["screen","-d","-m","-S","ftp_server_screen","python3","{}/server.py".format(PATH),password])
    sys.stdout.write("Started server. Session expire on logout and after 30 minutes inactive. Temporary password is : \n\npassword = {}\n".format(password))



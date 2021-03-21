#!/usr/bin/python3
import os, sys
os.chdir(sys.path[0])
server_version = "paper-1.16.5-562.jar"
if ".mc" in os.popen("screen -ls").read() and ".mc" not in os.popen("echo $STY").read():
	print("Server already running.\nType 'screen -x mc' to open the console")
else:
	os.system("echo [] > ops.json")
	os.system("screen -d -m -S \"mc\" /usr/lib/jvm/jdk-11.0.9/bin/java -XX:OnOutOfMemoryError=\"/home/minecraft/server/start.sh ; kill -9 %p\" -jar {} --nogui".format(server_version))

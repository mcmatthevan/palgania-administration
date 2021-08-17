#!/usr/bin/python3
import os, sys
leters = "mc"
server_version = "forge-1.16.5-36.2.2.jar"
ram = "500M","2048M"

os.chdir(sys.path[0])
if "."+leters in os.popen("screen -ls").read() and "."+leters not in os.popen("echo $STY").read():
	print("Server already running.\nType 'screen -x "+leters+"' to open the console")
else:
	os.system("echo [] > ops.json")
	os.system("screen -d -m -S \""+leters+"\" /usr/lib/jvm/jdk-11.0.9/bin/java -Xmx"+ram[1]+" -Xms"+ram[0]+" -XX:OnOutOfMemoryError=\"python3"+__file__+" ; kill -9 %p\" -jar {} --nogui".format(server_version))

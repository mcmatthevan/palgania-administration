import os, sys
os.chdir(sys.path[0])
with open("/home/minecraft/server/password.txt","r") as fichier:
	password = fichier.read()
os.system("openssl enc -e -aes-256-cbc -in server_sav -out server_sav.enc -pass pass:{}".format(password))

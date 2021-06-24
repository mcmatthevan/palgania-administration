#!/usr/bin/python3
import os
from time import strftime as t
os.chdir("/home/minecraft/palgania_save/github_saves/")
date = "{}/{}/{} {}:{}".format(t("%d"),t("%m"),t("%Y"),t("%H"),t("%M"))
for i,fichier in enumerate(sorted(os.listdir())):
	os.system("git add {}".format(fichier))
	os.system("git commit -am \"({}) {}\"".format(i+1,date))
	os.system("git push")

#!/usr/bin/python3
import os
from time import strftime as t
os.chdir("/home/minecraft/palgania_save/github_saves/")
print(os.listdir("../temp_saves/"))
print(os.listdir())
if len(os.listdir("../temp_saves/")) < len(os.listdir()):
	for f in os.listdir():
		if f not in os.listdir("../temp_saves/"):
			os.system("git rm --cached {}".format(f))
			os.system("rm {}".format(f))
	os.system("git commit -am \"clear file commit\"")
	os.system("git push")
os.system("mv ../temp_saves/* ./")
os.system("rmdir ../temp_saves/")
date = "{}/{}/{} {}:{}".format(t("%d"),t("%m"),t("%Y"),t("%H"),t("%M"))
for i,fichier in enumerate(sorted(os.listdir())):
	os.system("git add {}".format(fichier))
	os.system("git commit -am \"({}) {}\"".format(i+1,date))
	os.system("git push")

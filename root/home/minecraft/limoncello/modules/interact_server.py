from subprocess import Popen as pop
from subprocess import PIPE
import re
import csv
import json
import os
import requests

L_PATH = os.path.abspath(os.path.dirname(__file__) + "/..")
PATH = "/home/minecraft/server"

def getInfos(pseudo):
    uuid = getUUID(pseudo)
    dic = {
        "uuid": uuid,
        "lastLogout": getLastLogout(uuid)
    }
    if uuid is None:
        return dic
    dic["pseudo"] = requests.get("https://sessionserver.mojang.com/session/minecraft/profile/{}".format(uuid)).json()["name"]
    banned = open("{}/banned-players.json".format(PATH),"r").read()
    if re.search(r"(?i)\"name\":\s*\"{}\"".format(pseudo),banned):
        banned = json.loads(banned)
        for i,pse in enumerate(banned):
            if pseudo.lower() == pse["name"].lower():
                break
        dic["banned"] = {
            "created": banned[i].get("created"),
            "expires": banned[i].get("expires"),
            "reason": banned[i].get("reason"),
            "source": banned[i].get("source")
        }
        del banned
    else:
        del banned
        dic["banned"] = None
    try:
        dic["firstjoin"] = json.loads(open("{}/firstjoins.json".format(PATH),"r").read()).get(dic["uuid"])
    except FileNotFoundError:
        dic["firstjoin"] = None
    os.chdir(L_PATH)
    os.system("mkdir -p userbios")
    if "{}.json".format(pseudo.lower()) in os.listdir("userbios"):
        dic["bio"] = json.loads(open("userbios/{}.json".format(pseudo.lower()),"r").read())
    else:
        dic["bio"] = None
    return dic

def getLogs(day,srch,limit=50):
    if day == "all":
        return "ERR_ALL"
    else:
        p = pop("mclogs NFI {} {}".format(day,srch.replace(" ","\\s")).split(" "),stdout=PIPE,stderr=PIPE)
        result = p.communicate()[0].decode()
        if len(result.split("\n")) > limit:
            return "ERR_TOO_MANY_LINES"
        else:
            return re.sub(r"([0-9]{1,3}\.){3}[0-9]{1,3}","XX.XX.XX.XX",result).replace("<","&lt;").replace(">","&gt;").replace("\n","<br>")\
                                                                              .replace("\x1b[01;31m\x1b[K","<span style='color:red;font-weight:bold;'>")\
                                                                              .replace("\x1b[m\x1b[K","</span>")\
                                                                              .replace("\x1b[32m","<span style='color:green;'>")\
                                                                              .replace("\x1b[0m","</span>")

def getIp(pseudo):
    uuid = getUUID(pseudo)
    if uuid is None:
        return "BAD_PSEUDO"
    return pop("grep ipAddress {}/plugins/Essentials/userdata/{}.yml".format(PATH,uuid).split(" "),stdout=PIPE,stderr=PIPE).communicate()[0].decode().replace("ipAddress: ","").replace("\n","")

def getLastLogout(uuid):
    if "{}.yml".format(uuid) in os.listdir("{}/plugins/Essentials/userdata/".format(PATH)):
        return int(pop("grep logout: {}/plugins/Essentials/userdata/{}.yml".format(PATH,uuid).split(" "),stdout=PIPE,stderr=PIPE).communicate()[0].decode().replace("logout: ","").replace("\n",""))
    else:
        return None

def getUUID(pseudo):
    with open("{}/plugins/Essentials/usermap.csv".format(PATH),"r") as csvfile:
        reader = tuple(csv.reader(csvfile,delimiter=",",quotechar="|"))
    for row in reader:
        if row[0] == pseudo.lower().replace("*","_"):
            return row[1]

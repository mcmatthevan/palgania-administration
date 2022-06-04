from subprocess import Popen as pop
from subprocess import PIPE
import re
import csv
import json
import yaml
import os
import requests
import time

L_PATH = os.path.abspath(os.path.dirname(__file__) + "/..")
PATHS = ("/home/minecraft/server",
         "/home/minecraft/atestpl")
rshellpath = "/home/minecraft/rshell/rshell.py"
botdir = "/home/minecraft/bot"

def getDiscord(uuid):
    dic = yaml.safe_load(open(botdir+"/usermap.yaml","r").read())
    for item in dic:
        if dic[item] == uuid.strip():
            return item
    return None

def suspension(player,temp):
    player = player.lower()
    if "admin" in [parent["group"] for parent in json.loads(open("{}/plugins/LuckPerms/json-storage/users/{}.json".format(PATHS[0], getUUID(player)), "r").read()).get("parents")]:
        os.system("mcsend deop {}".format(player))
        os.system("mcsend lp user {} perm settemp minecraft.command.op false {}s".format(player,temp))
        os.system("mcsend gamemode survival {}".format(player))
        return "L'administrateur {} a été suspendu pour une durée de {} secondes".format(player,temp)
    else:
        return "ERR_NOT_ADMIN"

def setPerm(player, perm, temp=3600, group="modo"):
    player = player.lower()
    try:
        if group in [parent["group"] for parent in json.loads(open("{}/plugins/LuckPerms/json-storage/users/{}.json".format(PATHS[0], getUUID(player)), "r").read()).get("parents")]:
            p = pop(["mclogs", "NFI"], stdout=PIPE, stderr=PIPE)
            first = len(p.communicate()[0].decode())
            os.system("mcsend lp user {} perm settemp {} true {}s".format(
                player, perm, temp))
            time.sleep(0.2)
            p = pop(["mclogs", "NFI"], stdout=PIPE, stderr=PIPE)
            return p.communicate()[0].decode()[first:]
        else:
            return "ERR_BAD_GROUP"
    except FileNotFoundError:
        return "ERR_BAD_USER"


def vote_award(pseudo,votesnb):
    os.system(f"mcsend tpcredits add {pseudo} 5")
    os.system(f"mcsend advancement grant {pseudo} only palg_adv:success/vote0")
    if votesnb >= 7:
        os.system(f"mcsend advancement grant {pseudo} only palg_adv:success/vote1")
    return "OK"

def getInfos(pseudo,is_uuid=False):
    if is_uuid:
        uuid = pseudo
    else:
        uuid = getUUID(pseudo)
    if uuid is None:
        return {"uuid": None}
    dic = {
        "uuid": uuid,
        "discord": getDiscord(uuid),
        "lastLogout": time.strftime("%Y-%m-%d", time.localtime(getLastLogout(uuid)//1000))
    }
    import simplejson
    try:
        dic["pseudo"] = requests.get(
            "https://sessionserver.mojang.com/session/minecraft/profile/{}".format(uuid)).json()["name"]
    except simplejson.errors.JSONDecodeError:
        dic["pseudo"] = pseudo
    if is_uuid:
        pseudo = dic['pseudo']
    banned = open("{}/banned-players.json".format(PATHS[0]), "r").read()
    if re.search(r"(?i)\"name\":\s*\"{}\"".format(pseudo), banned):
        banned = json.loads(banned)
        for i, pse in enumerate(banned):
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
        dic["firstjoin"] = json.loads(
            open("{}/firstjoins.json".format(PATHS[0]), "r").read()).get(dic["uuid"])
    except FileNotFoundError:
        dic["firstjoin"] = None
    os.chdir(L_PATH)
    os.system("mkdir -p userbios")
    if "{}.json".format(pseudo.lower()) in os.listdir("userbios"):
        dic["bio"] = json.loads(
            open("userbios/{}.json".format(pseudo.lower()), "r").read())
    else:
        dic["bio"] = None
    return dic


def getLogs(day, srch, limit=50):
    if day == "all":
        return "ERR_ALL"
    else:
        p = pop("mclogs NFI {} {}".format(day, srch.replace(
            " ", "\\s")).split(" "), stdout=PIPE, stderr=PIPE)
        result = p.communicate()[0].decode()
        if len(result.split("\n")) > limit:
            return "ERR_TOO_MANY_LINES"
        else:
            return re.sub(r"([0-9]{1,3}\.){3}[0-9]{1,3}", "XX.XX.XX.XX", result).replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")\
                .replace("\x1b[01;31m\x1b[K", "<span style='color:red;font-weight:bold;'>")\
                .replace("\x1b[m\x1b[K", "</span>")\
                .replace("\x1b[32m", "<span style='color:green;'>")\
                .replace("\x1b[0m", "</span>")


def getIp(pseudo):
    uuid = getUUID(pseudo)
    if uuid is None:
        return "BAD_PSEUDO"
    return pop("grep ip-address {}/plugins/Essentials/userdata/{}.yml".format(PATHS[0], uuid).split(" "), stdout=PIPE, stderr=PIPE).communicate()[0].decode().replace("ip-address: ", "").replace("\n", "")


def getLastLogout(uuid):
    for path in PATHS:
        if "{}.yml".format(uuid) in os.listdir("{}/plugins/Essentials/userdata/".format(path)):
            return int(pop("grep logout: {}/plugins/Essentials/userdata/{}.yml".format(path, uuid).split(" "), stdout=PIPE, stderr=PIPE).communicate()[0].decode().replace("logout: ", "").replace("\n", ""))
    return None


def getUUID(pseudo):
    for path in PATHS:
        with open("{}/plugins/Essentials/usermap.csv".format(path), "r") as csvfile:
            reader = tuple(csv.reader(csvfile, delimiter=",", quotechar="|"))
        for row in reader:
            if row[0] == pseudo.lower().replace("*", "_"):
                return row[1]


def addKey(sshkey, user):
    os.system("mkdir -p ~/.ssh/")
    os.system("touch ~/.ssh/authorized_keys")
    perm = getattr(user, "consolePerms")
    if perm is None:
        perm = "default"
    open(os.path.expanduser("~/.ssh/authorized_keys"), "a").write(
        '\ncommand="{} {} {} $SSH_ORIGINAL_COMMAND" {}'.format(rshellpath, perm, user.username, sshkey))
    return "OK"

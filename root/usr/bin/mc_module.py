import yaml

def mcGetLeter(argv,delete=True):
    serverspath = "/home/minecraft/palgservers"

    aliases = yaml.safe_load(open(serverspath+"/.alias.yaml","r").read())
    aliasesdirs = [aliases[alias] for alias in aliases]

    leters = None
    toDel = None
    for i,arg in enumerate(argv):
        if arg[0:2] == "--":
            if delete:
                toDel = i
            leters = arg[2:]
            if leters in aliases.keys():
                serverdir = serverspath + "/" + aliases[leters]
            elif leters in aliasesdirs:
                leters = list(aliases.keys())[aliasesdirs.index(leters)]
                serverdir = serverspath + "/" + aliases[leters]
            else:
                serverdir = serverspath + "/" + leters
            break
    if delete and toDel is not None:
        del argv[i]
    del aliasesdirs

    if leters is None:
        leters = "mc"
        serverdir = serverspath + "/" + aliases[leters]
    return leters,serverdir

from base_commands import *

FTPPATH = "/home/minecraft/ftp"

class Commands(BaseCommands):
   def openftp(self):
      os.system("python3 {}/openftp.py".format(FTPPATH))
commands = Commands()

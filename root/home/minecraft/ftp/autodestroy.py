import os
import re
from subprocess import Popen as pop
from subprocess import PIPE

def configure(tps):
    p = pop("at now + {}".format(tps).split(" "),stdin=PIPE,stdout=PIPE,stderr=PIPE)
    return int(re.search(r"job\s+([0-9]+)\s+at",p.communicate(input="kill {}\n".format(os.getpid()).encode())[1].decode()).group(1))

def cancel(id):
    os.system("atrm {}".format(id))
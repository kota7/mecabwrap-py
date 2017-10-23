# -*- coding: utf-8 -*-


import subprocess
import re
from .globals import get_mecab


def mecab_exists():
    command = [get_mecab(), "-v"] 
    try:
        p = subprocess.Popen(command, stdout=subprocess.PIPE)
    except FileNotFoundError:
        return False

    out, err = p.communicate()
    out = out.decode().strip()
    reg  = re.match(r'mecab', out)
    return (reg is not None)




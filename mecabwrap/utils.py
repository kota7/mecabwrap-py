# -*- coding: utf-8 -*-


import subprocess
import re
from .globals import get_mecab


def mecab_exists():
    command = [get_mecab(), "-v"] 
    try:
        p = subprocess.run(command, stdout=subprocess.PIPE)
    except FileNotFoundError:
        return False

    mess = p.stdout.decode().strip()
    reg  = re.match(r'mecab', mess)
    return (reg is not None)




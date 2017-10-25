# -*- coding: utf-8 -*-


import subprocess
import re
from .config import get_mecab


def mecab_exists():
    """
    detect if mecab command exists
    
    :return: True or False
    """
    
    command = [get_mecab(), "-v"] 
    try:
        p = subprocess.Popen(command, stdout=subprocess.PIPE)
    except OSError:
        return False

    out, err = p.communicate()
    out = out.decode().strip()
    reg  = re.match(r'mecab', out)
    return (reg is not None)


def detect_mecab_enc(*args):
    """
    detect the mecab's dictionary charset (encoding)
    
    :param *args:  MeCab options; only `-d` option (systen dicdir) is used
    
    :return: string
    """
    
    # get -d option if any
    # note that mecab overwrites options given later
    dopt = None
    for i in range(len(args)):
        a = args[i]
        if a == '-d' or a == '--dicdir':
            assert i + 1 < len(args)
            dopt = args[i+1]
        elif a[0:2] == '-d':         # -d option with no space
            dopt = a[2:]
        elif a[0:9] == '--dicdir=':  # --dicdir option with no space
            dopt = a[9:]
    if dopt is not None:
        dopt = dopt.strip()
    
    assert mecab_exists(), "`%s` not found" % get_mecab()
    command = [get_mecab(), '-D']
    if dopt is not None:
        command += ['-d', dopt]
        
    p = subprocess.Popen(command, stdout=subprocess.PIPE)
    out, err = p.communicate()
    out = out.decode()
       
    reg = re.search(r'\bcharset:\s*([^\s]+)', out)
    assert reg is not None, "charset is not found\n  " + out
    return reg.group(1)
    
    
    
def _no_mecab_message():
    out = ['* `%s` is not recognized as a valid MeCab command' % get_mecab(),
           '',
           '* to install MeCab:',
           ' - Ubuntu',
           '  $ sudo apt-get install mecab libmecab-dev mecab-ipadic-utf8',
           ' - OSX', 
           '  $ brew install mecab mecab-ipadic',
           ' - Windows',
           '  Run the installer at https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7WElGUGt6ejlpVXc',
           '', 
           '* to configure the location of `mecab` program:',
           ' >>> from mecabwrap.config import set_mecab',
           ' >>> set_mecab("<path-to-mecab-binary>")']
    return '\n'.join(out)

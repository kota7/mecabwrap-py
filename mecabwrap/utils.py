# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import re
import argparse
from logging import getLogger
from .config import get_mecab, get_mecab_config

logger = getLogger(__name__)

def mecab_exists():
    """
    check if mecab command exists
    
    :return: bool
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


def mecab_config_exists():
    """
    check if mecab-config command exists
    
    :return: bool
    """
    command = [get_mecab_config(), "--version"]
    try:
        p = subprocess.Popen(command, stdout=subprocess.PIPE)
    except OSError:
        return False

    out, err = p.communicate()
    out = out.decode().strip()
    logger.debug("Result of `mecab-config --version`: %s", out)
    reg  = re.match(r'[\d\.]+', out)
    return (reg is not None)


def find_dictionary(dictionary):
    """
    find dictionary path
    
    :param dictionary:  Either the path to the dictionary directory
                        or sub-directory name under the mecab's dicdir
    
    :return:  string of the full path to the dictionary directory
              or None if dictionary not found
    """
    # check if this is already a valid path to a directory
    logger.debug("checking existence of `%s`", dictionary)
    if os.path.isdir(dictionary):
        return os.path.abspath(dictionary)
    
    # we need mecab-config to find the default directory location
    if not mecab_config_exists():
        logger.warning("mecab-config is not found." + \
                       "please provide the path to the dictionary directory")
        logger.debug("`%s` is not a valid path" % dictionary)                       
        return None
    # check if the directory exists under the mecab's default directory
    dictionary2 = os.path.join(get_mecab_dicdir(), dictionary)
    logger.debug("checking existence of `%s`", dictionary2)
    if os.path.isdir(dictionary2):
        return os.path.abspath(dictionary2)
    # not found
    logger.debug("Neither `%s` nor `%s` is a valid path" % (dictionary, dictionary2))
    return None

def get_mecab_dicdir():
    """
    detect the mecab's default dictionary directory
    
    :return:  string
    """
    assert mecab_config_exists(), "`%s` not found" % get_mecab_config()
    command = [get_mecab_config(), '--dicdir']
    p = subprocess.Popen(command, stdout=subprocess.PIPE)
    out, err = p.communicate()
    out = out.decode().strip()
    return out

def detect_mecab_enc(*args):
    """
    detect the mecab's dictionary charset (encoding)
    
    :param *args:  MeCab options; only `-d` option (systen dicdir) is used
    
    :return: string
    """
    
    # get -d option if any
    dopt = get_mecab_opt('-d', *args)
    
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
    
    

# map short option name to long option name, type and store_true
# set str type as unicode for python2
_str_type = unicode if sys.version_info[0] == 2 else str
_MECAB_OPTIONS = { 
    '-r'  : ('--rcfile', _str_type)
    ,'-d' : ('--dicdir', _str_type)
    ,'-u' : ('--userdic', _str_type)
    ,'-l' : ('--lattice-level', int)
    ,'-D' : ('--dictionary-info', None)
    ,'-O' : ('--output-format-type', _str_type)
    ,'-a' : ('--all-morphs', None)
    ,'-N' : ('--nbest', int)
    ,'-p' : ('--partial', None)
    ,'-m' : ('--marginal', None)
    ,'-M' : ('--max-groupint-size', int)
    ,'-F' : ('--node-format', _str_type)
    ,'-U' : ('--unk-format', _str_type)
    ,'-B' : ('--bos-format', _str_type)
    ,'-E' : ('--eos-format', _str_type)
    ,'-S' : ('--eon-format', _str_type)
    ,'-x' : ('--unk-feature', _str_type)
    ,'-b' : ('--input-buffer-size', int)
    ,'-P' : ('--dump-config', None)
    ,'-C' : ('--allocate-sentence', None)
    ,'-t' : ('--theta', float)
    ,'-c' : ('--cost-factor', int)
    ,'-o' : ('--output', _str_type)
    ,'-v' : ('--version', None)
    #,'-h' : ('--help', None)
}
del(_str_type)


_MECAB_ARG_PARSER = argparse.ArgumentParser()
_MECAB_ARG_PARSER.add_argument('files', nargs='*')
for short, item in _MECAB_OPTIONS.items():
    long_, typ = item
    if item[1] is None:
        _MECAB_ARG_PARSER.add_argument(short, long_, action='store_true')
    else:
        _MECAB_ARG_PARSER.add_argument(short, long_, type=typ)


def get_mecab_opt(option, *args):
    """
    parse and return mecab argument

    :param opt:   string of target option; e.g. '-u', '--dicdir'
    :param value: boolean; indicates if the option has a value 
    :param *args: arguments passed to mecab

    :return:  if value is True, then returns the option value if specified,
              or None if not specified;
              if value is False, then returns boolean indicating
              if the option is specified
    """
    try:
        args = _MECAB_ARG_PARSER.parse_args(args)
    except Exception as e:
        logger.error(e)
        return None

    # convert short option to long
    if option[0:2] != '--':
        option = _MECAB_OPTIONS[option][0]
    name = option[2:].replace('-', '_')
    try:
        ret = vars(args)[name]
    except Exception as e:
        logger.error(e)
        return None
    return ret

    
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

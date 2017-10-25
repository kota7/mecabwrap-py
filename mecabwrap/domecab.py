# -*- coding: utf-8 -*-

import os
import sys
import subprocess
from tempfile import mkstemp
from .config import get_mecab
from .utils import mecab_exists, detect_mecab_enc, _no_mecab_message


# check the mecab command when imported
if not mecab_exists():
    print(_no_mecab_message())



def do_mecab(x, *args, **kwargs):
    """
    call mecab
    
    :param x:         a unicode string
    :param *args:     options of mecab; see `mecab --help`
    :param **kwargs:  other options
                      - outpath (default: None) : if None, outcome is returned;
                        otherwise, outcome is written to the file
                      - mecab_enc (default: None): encoding of mecab; if None,
                        automatically detect the encoding

    :return:          unicode string;
                      if not successful, error message is returned;
                      if successful and outpath is not given, then
                      mecab outcome is returned;
                      if successful and outpath is givem then
                      the results are written to the file and 
                      an empty string is returned
    """
    
    # return if mecab does not exist
    if not mecab_exists():
        print(_no_mecab_message())
        return u''
        
        
    outpath   = kwargs.pop('outpath', None)
    mecab_enc = kwargs.pop('mecab_enc', None)
    
    # detect enc
    if mecab_enc is None:
        mecab_enc = detect_mecab_enc(*args)


    if sys.version_info[0] == 3:
        assert isinstance(x, str), "x must be string"
        assert outpath is None or isinstance(outpath, str)
    elif sys.version_info[0] == 2:
        assert isinstance(x, unicode), "x must be unicode string"
        assert outpath is None or \
               isinstance(outpath, str) or \
               isinstance(outpath, unicode) 
    else:
        print("do we have python 4 now?")
            

    # conduct mecab if outfile is not None, 
    # then write it to the file;
    # otherwise do with no option
    command = [get_mecab()] + list(args)
    if outpath is not None:
        command += ["-o", outpath]

    p = subprocess.Popen(command, 
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE)
    
    x = x.strip()
    if len(x) > 0:
        out, err = p.communicate((x + u'\n').encode(mecab_enc))
    else:
        out, err = p.communicate()
    
    #p.terminate()
    
    return out.decode(mecab_enc)


def do_mecab_vec(x, *args, **kwargs):
    """
    call mecab with multiple inputs 
    
    :param x:         iterable of unicode strings
    :param *args:     options to mecab; see `mecab --help`
    :param **kwargs:  other options
                      - outpath (default: None) : if None, outcome is returned;
                        otherwise, outcome is written to the file
                      - mecab_enc (default: None) : encoding of mecab
 
    :return:          result of mecab call in unicode string
    """
    
    # return if mecab does not exist
    if not mecab_exists():
        print(_no_mecab_message())
        return u''

    outpath   = kwargs.pop('outpath', None)
    mecab_enc = kwargs.pop('mecab_enc', None)

    # detect dictionary encoding if not given
    if mecab_enc is None:
        mecab_enc = detect_mecab_enc(*args)

    # write x to a temp file
    fd, infile = mkstemp()
    with open(infile, "wb") as f:
        for txt in x:
            f.write((txt + '\n').encode(mecab_enc))
    
    out = do_mecab(u'', infile, *args, outpath=outpath, mecab_enc=mecab_enc)
    
    # make sure the temp file is removed    
    os.close(fd)
    os.remove(infile)
    
    return out


def do_mecab_iter(x, *args, **kwargs):
    """
    call mecab with multiple inputs and get results one by one

    :param x:         iterable
    :param *args:     options to mecab; see `mecab --help`
    :param **kwargs:  other options.
                      - byline (default: False) : if true, 
                        the returned generator yields one line at at time;
                        otherwise, it yields a chunk up to 'EOS' at a time
                      - mecab_enc (default: None) : encoding of mecab

    :return:          generator of mecab outcomes
    """
    
    # return if mecab does not exist
    if not mecab_exists():
        print(_no_mecab_message())
        return

    byline    = kwargs.pop('byline', False)
    mecab_enc = kwargs.pop('mecab_enc', None)

    # detect dictionary encoding if not given
    if mecab_enc is None:
        mecab_enc = detect_mecab_enc(*args)

    # make a temp file for writing output
    fd, ofile = mkstemp()

    do_mecab_vec(x, *args, outpath=ofile, mecab_enc=mecab_enc)


    with open(ofile, 'rb') as f:
        if byline:
            for line in f:
                yield line.decode(mecab_enc).strip()
        else:
            doc = b''
            for line in f:
                doc += line
                tmp = line.decode(mecab_enc).strip()
                if len(tmp) >= 3 and tmp[-3:] == 'EOS':
                    yield doc.decode(mecab_enc).strip()
                    doc = b''
    os.close(fd)
    os.remove(ofile)


    

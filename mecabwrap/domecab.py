# -*- coding: utf-8 -*-

import os
import sys
import subprocess
from tempfile import mkstemp


def do_mecab(x, *args, **kwargs):
    """
    call mecab
    
    :param x:         a string
    :param *args:     options of mecab; see `mecab --help`
    :param **kwargs:  other options
                      - outpath (default: None) : if None, outcome is returned;
                        otherwise, outcome is written to the file
                      - mecab_enc (default: 'utf8'): encoding of mecab
                      - encoding, error: if `x` is bytes type, then passed to
                        `bytes.decode` for casting to unicode;

    :return:          string;
                      if not successful, error message is returned;
                      if successful and outpath is not given, then
                      mecab outcome is returned;
                      if successful and outpath is givem then
                      the results are written to the file and 
                      an empty string is returned
    """
    
    # make sure that x is a unicode string
    if isinstance(x, bytes):
        args = dict((key, kwargs[key]) for key in kwargs if key in ['encoding', 'errors'])
        x = x.decode(**args)
        
    
    outpath   = kwargs.pop('outpath', None)
    mecab_enc = kwargs.pop('mecab_enc', 'utf8')

    if sys.version_info[0] == 3:
        assert isinstance(x, str), "x must be string"
        assert outpath is None or isinstance(outpath, str)
    elif sys.version_info[0] == 2:
        assert isinstance(x, unicode), "x must be unicode string"
        assert outpath is None or isinstance(outpath, str) or isinstance(outpath, unicode) 
    else:
        print("do we have python 4 now?")
            
    # conduct mecab if outfile is not None, 
    # then write it to the file;
    # otherwise do with no option
    command = ["mecab"] + list(args)
    if outpath is not None:
        command += ["-o", outpath]

    p = subprocess.Popen(command, 
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE)

    out, err = p.communicate((x + '\n').encode(mecab_enc))
    #p.terminate()
    
    return out.decode(mecab_enc)


def do_mecab_vec(x, *args, **kwargs):
    """
    call mecab with multiple inputs 
    
    :param x:         iterable
    :param *args:     options to mecab; see `mecab --help`
    :param **kwargs:  other options
                      - outpath (default: None) : if None, outcome is returned;
                        otherwise, outcome is written to the file
                      - mecab_enc (default: 'utf8') : encoding of mecab
                      - encoding, error: if `x` is bytes type, then passed to
                        `bytes.decode` for casting to unicode;

    :return:          string of the output of mecab call
    """
    
    decode_args = dict((key, kwargs[key]) for key in kwargs if key in ['encoding', 'errors'])

    
    outpath   = kwargs.pop('outpath', None)
    mecab_enc = kwargs.pop('mecab_enc', 'utf8')

    # write x to a temp file
    fd, infile = mkstemp()
    with open(infile, "wb") as f:
        for txt in x:
            # make sure that txt is a unicode string;
            # this may look redundant as txt is encoded to bytes anyways,
            # but is necessary since input encoding and mecab encoding may differ
            if isinstance(txt, bytes):                
                txt = txt.decode(**decode_args)
            f.write((txt + '\n').encode(mecab_enc))

    # call mecab
    command = ['mecab', infile] + list(args)
    if outpath is not None:
        command += ['-o', outpath]

    p = subprocess.Popen(command, 
                         stdin=subprocess.PIPE, 
                         stdout=subprocess.PIPE)
    out, err = p.communicate()
    #p.terminate()
    
    os.close(fd)
    os.remove(infile)
    
    return out.decode(mecab_enc) 



def do_mecab_iter(x, *args, **kwargs):
    """
    call mecab with multiple inputs and get results one by one

    :param x:         iterable
    :param *args:     options to mecab; see `mecab --help`
    :param **kwargs:  other options.
                      - byline (default: False) : if true, 
                        the returned generator yields one line at at time;
                        otherwise, it yields a chunk up to 'EOS' at a time
                      - mecab_enc (default: 'utf8') : encoding of mecab
                      - encoding, error: if `x` is bytes type, then passed to
                        `bytes.decode` for casting to unicode;

    :return:          generator of mecab outcomes
    """

    byline    = kwargs.pop('byline', False)
    mecab_enc = kwargs.pop('mecab_enc', 'utf8')

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


    

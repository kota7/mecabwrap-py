# -*- coding: utf-8 -*-

import os
import subprocess
from tempfile import mkstemp


def do_mecab(x, *args, outpath=None):
    """
    call mecab
    
    :param x:        a string
    :param outpath:  None or a valid file path
    :param *args:    options of mecab; see `mecab --help`
    
    :return:         if not successful, error message is returned;
                     if successful and outpath is not given, then
                     mecab outcome is returned as bytes;
                     if successful and outpath is givem then
                     the results are written to the file and 
                     an empty byte is returned
    """

    assert isinstance(x, str), "x must be str"
    assert outpath is None or isinstance(outpath, str)
    
    # conduct mecab if outfile is not None, 
    # then write it to the file;
    # otherwise do with no option
    command = ["mecab", *args]
    if outpath is not None:
        command += ["-o", outpath]
    p = subprocess.Popen(command, 
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE)

    out, err = p.communicate((x + '\n').encode())
    p.terminate()
    
    return out


def do_mecab_vec(x, *args, outpath=None):
    """
    call mecab with multiple inputs 
    
    :param x:       iterable
    :param *args:   options to mecab; see `mecab --help`
    :param outpath: if None, outcome is returned as a combined binary string;
                    if str indiccating a valid file path, 
                    the outcome is written to the file
    :return:        a binary string of output of mecab call
    """

    # write x to a temp file
    _, infile = mkstemp()
    with open(infile, "wt") as f:
        for txt in x:
            f.write(txt + '\n')

    # call mecab
    command = ['mecab', infile, *args]
    if outpath is not None:
        command += ['-o', outpath]

    p = subprocess.Popen(command, 
                         stdin=subprocess.PIPE, 
                         stdout=subprocess.PIPE)
    out, err = p.communicate()
    p.terminate()
    os.remove(infile)
    
    return out 



def do_mecab_iter(x, *args, byline=False):
    """
    call mecab with multiple inputs and get results one by one

    :param x:        iterable
    :param *args:    options to mecab; see `mecab --help`
    :param byline:   if true, generator yields one line at at time;
                     otherwise, it yields a chunk up to 'EOS' at a time
    
    :return:         generator of mecab outcomes
    """

    # make a temp file for writing output
    _, ofile = mkstemp()

    do_mecab_vec(x, *args, outpath=ofile)


    with open(ofile, 'rt') as f:
        if byline:
            for line in f:
                yield line.strip()
        else:
            doc = ''
            for line in f:
                doc += line
                tmp = line.strip()
                if len(tmp) >= 3 and tmp[-3:] == 'EOS':
                    yield doc.strip()
                    doc = ''
    os.remove(ofile)


    

# -*- coding: utf-8 -*-

import subprocess


def do_mecab(x, *args, outpath=None):
    """
    call mecab
    
    :param x:        a string
    :param outpath:  None or a valid file path
    :param *args:    options of mecab; see `mecab --help`
    
    :returns:        if not successful, error message is returned;
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


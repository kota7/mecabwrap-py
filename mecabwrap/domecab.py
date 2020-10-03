# -*- coding: utf-8 -*-

import os
import re
import sys
from logging import getLogger
import subprocess
import codecs
import warnings
from tempfile import mkstemp
from .config import get_mecab
from .utils import mecab_exists, detect_mecab_enc, find_dictionary
from .utils import _no_mecab_message, get_mecab_opt

logger = getLogger(__name__)

# check the mecab command when imported
if not mecab_exists():
    print(_no_mecab_message())



# note: I use **kwargs instead of explicit keyword arguments
#       because older versions of python does not allow
#       explicit keyword arguments follow *args.


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

    outpath    = kwargs.pop('outpath', None)
    mecab_enc  = kwargs.pop('mecab_enc', None)
    dictionary = kwargs.pop('dictionary', None)
    
    opt = get_mecab_opt('-o', *args)
    if opt and outpath:
        logger.warning('both `-o` and `outpath` are given, `outpath` is ignored')
        warnings.warn('both `-o` and `outpath` are given, `outpath` is ignored')
        outpath = None
        
    dic = get_mecab_opt('-d', *args)
    if dic and dictionary:
        logger.warning('both -d and dictionary are given, dictionary is ignored')
        warnings.warn('both -d and dictionary are given, dictionary is ignored')
        dictionary = None
    if dictionary:
        dictionary = find_dictionary(dictionary)
        assert dictionary is not None, ("dictionary `%s` not found" % dictionary)
        logger.debug("Dicationary found: `%s`" % dictionary)
        

    # detect enc
    if mecab_enc is None:
        mecab_enc = detect_mecab_enc(*args)

    if sys.version_info[0] == 2:
        assert isinstance(x, unicode), "x must be unicode string"
        assert outpath is None or \
               isinstance(outpath, str) or \
               isinstance(outpath, unicode) 
        assert dictionary is None or \
               isinstance(dictionary, str) or \
               isinstance(dictionary, unicode) 
    else:
        assert isinstance(x, str), "x must be string"
        assert outpath is None or isinstance(outpath, str)
        assert dictionary is None or isinstance(dictionary, str)
    
    # conduct mecab if outfile is not None, 
    # then write it to the file;
    # otherwise do with no option
    command = [get_mecab()] + list(args)
    if outpath is not None:
        command += ["-o", outpath]
    if dictionary is not None:
        command += ["-d", dictionary]
    
    # for python 2.x, mecab_enc <> utf8,
    # args with unicode raise UnicodeEncodeError
    # a workaround seems to be converting them to bytes of mecab_enc
    if sys.version_info[0] == 2 and codecs.lookup(mecab_enc).name != 'utf-8':
        command = [a.encode(mecab_enc) if isinstance(a, unicode) else a \
                   for a in command]

    p = subprocess.Popen(command, 
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE)
    
    x = x.strip()
    if len(x) > 0:
        out, err = p.communicate((x + u'\n').encode(mecab_enc))
    else:
        out, err = p.communicate()
    #p.terminate()
    
    return out.decode(mecab_enc, 'ignore')


def do_mecab_vec(x, *args, **kwargs):
    """
    call mecab with multiple inputs 
    
    :param x:         iterable of unicode strings
    :param *args:     options to mecab; see `mecab --help`
    :param **kwargs:  other options
                      - outpath (default: None) : if None, outcome is returned;
                        otherwise, outcome is written to the file
                      - mecab_enc (default: None) : encoding of mecab
                      - auto_buffer_size (default: False): if True,
                        adjust buffer size to the necessary size
                      - truncate (default: False): if True,
                        input longer than the buffer size is truncated,
                        so that the output length is preserved
 
    :return:          result of mecab call in unicode string
    """
    
    # return if mecab does not exist
    if not mecab_exists():
        print(_no_mecab_message())
        return u''

    #outpath   = kwargs.pop('outpath', None)
    mecab_enc = kwargs.pop('mecab_enc', None)
    auto_buffer_size = kwargs.pop('auto_buffer_size', False)
    truncate = kwargs.pop('truncate', False)

    # detect dictionary encoding if not given
    if mecab_enc is None:
        mecab_enc = detect_mecab_enc(*args)

    # set "-b" option
    max_input_size = max(len(a.encode(mecab_enc)) for a in x)
    if auto_buffer_size:
        bopt_auto = max_input_size + 1
        logger.debug('bopt is automatically set to %d', bopt_auto)
    else:
        bopt_auto = None
    # check if -b option is given
    bopt_given = get_mecab_opt('-b', *args)
    
    if bopt_given and bopt_auto:
        # both given, used the auto one
        logger.warning('`-b` is auto-adjucted from %d to %d', 
                    bopt_given, bopt_auto)
        warnings.warn('`-b` is auto-adjucted from %d to %d' % \
                    (bopt_given, bopt_auto))

    default_buff_size = 8192
    maximum_buff_size = 8192 * 640
    # bopt_ is the buffer size to be used
    bopt_ = bopt_auto if bopt_auto else \
            bopt_given if bopt_given else \
            default_buff_size

    if bopt_ > maximum_buff_size:
        # fatal, cannot set this large buffer size
        logger.warning('%d is truncated to maximum possible buffer size (%d)',
                    bopt_, maximum_buff_size)
        warnings.warn('%d is truncated to maximum possible buffer size (%d)' % \
                      (bopt_, maximum_buff_size))
        bopt_ = maximum_buff_size
        
    # logging by the size situation
    if bopt_ <= max_input_size:
        logger.info(
            'buffer size (%d) <= max input size (%d)', bopt_, max_input_size)    
        if truncate:
            logger.info('some input text would be truncated')
        else:
            logger.warning('output would contain extra EOS')
            mess = 'buffer size (%d) <= max input size (%d)' % (bopt_, max_input_size)
            warnings.warn(
                'output would contain extra EOS, due to size overflow (%d >= %d)' % \
                (max_input_size, bopt_))
    else:
        logger.debug('buffer size (%d) > max input size (%d), which is safe', 
                     bopt_, max_input_size)    

    # write x to a temp file
    # this is slightly faster than passing input as is
    # when input size is very large
    fd, infile = mkstemp()
    logger.debug("Temporary input file: %s", infile)
    with open(infile, "wb") as f:
        xb = [a.replace('\n', ' ').encode(mecab_enc) for a in x] 
        if truncate:
            xb = [a[0:(bopt_ - 1)] for a in xb]
        txt = b'\n'.join(xb) + b'\n'
        f.write(txt)

    if bopt_auto:
        args = list(args) + ['-b', str(bopt_auto)]
    out = do_mecab(u'', infile, *args, mecab_enc=mecab_enc, **kwargs)

    # make sure the temp file is removed    
    os.close(fd)
    os.remove(infile)

    # pass the text directly
    # this is faster when input size is small
    #y = '\n'.join(a.replace('\n', ' ') for a in x) 
    #out = do_mecab(y, *args, outpath=outpath, mecab_enc=mecab_enc)
    
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
                      - auto_buffer_size (default: False): if True,
                        adjust buffer size to the necessary size
                      - truncate (default: False): if True,
                        input longer than the buffer size is truncated,
                        so that the output length is preserved

    :return:          generator of mecab outcomes
    """
    
    # return if mecab does not exist
    if not mecab_exists():
        print(_no_mecab_message())
        return

    byline = kwargs.pop('byline', False)
    mecab_enc = kwargs.pop('mecab_enc', None)
    outpath = kwargs.pop('outpath', None)

    # detect dictionary encoding if not given
    if mecab_enc is None:
        mecab_enc = detect_mecab_enc(*args)

    opt = get_mecab_opt('-o', *args)
    if opt:
        raise ValueError("`-o` option is not supported for `do_mecab_iter`")
    if outpath:
        raise ValueError("`outpath` option is not supported for `do_mecab_iter`")


    # make a temp file for writing output
    fd, ofile = mkstemp()
    logger.debug("Temporary output file %s:", ofile)
    
    # use temporary eos
    EOS = get_mecab_opt('-E', *args)
    EOS = 'EOS' if EOS is None else EOS.strip()
    EOS_tmp = '___TEMPORARYENDOFSENTENCE___'
    
    args = list(args) + ['-E', EOS_tmp + '\n']
    do_mecab_vec(
        x, *args, outpath=ofile, mecab_enc=mecab_enc, **kwargs)


    with open(ofile, 'rb') as f:
        if byline:
            for line in f:
                tmp = line.decode(mecab_enc, 'ignore').strip()
                tmp = tmp.replace(EOS_tmp, EOS)
                yield tmp
        else:
            doc = u''
            for line in f:
                tmp = line.decode(mecab_enc, 'ignore').strip()
                if tmp[(-len(EOS_tmp)):] == EOS_tmp:
                    tmp = tmp[0:(-len(EOS_tmp))] + EOS
                    doc += tmp
                    yield doc
                    doc = u''
                else:
                    doc += tmp + u'\n'
            if len(doc) > 0:
                yield doc

    os.close(fd)
    os.remove(ofile)


    

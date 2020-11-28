# -*- coding: utf-8 -*-


import sys
from collections import namedtuple
from .domecab import do_mecab, do_mecab_iter


Token = namedtuple("Token", [
    "surface"
    ,"pos"
    ,"pos1"
    ,"pos2"
    ,"pos3"
    ,"infl_type"
    ,"infl_form"
    ,"baseform"
    ,"reading"
    ,"phoenetic"
    # additional info available for unidic dictionary
    ,"lemma"          # goiso
    ,"lemma_reading"  # goiso reading
])

def str_token(token):
    fmt = u"%s\t" + u",".join([u"%s"] * (len(token)-1))    
    return fmt % tuple([u"*" if t is None else t for t in token])

def print_token(token):
    print(str_token(token))
    
def mecab_batch_iter(x, dictionary=None, mecab_enc=None, unidic_format=None,
                     format_func=None, pos_filter=None, filter_func=None):
    # todo: choose separaters that do not appear in x
    tokensep = chr(1)
    infosep = chr(2)
    
    if unidic_format is None and \
        (dictionary is not None and dictionary.find("unidic") >= 0):
        print("`unidic_format` is set to true")
        unidic_format = True
    
    if unidic_format:
        tmp = ["%m"] + ["%f[{}]".format(i) for i in range(6)] + \
          ["%f[10]", "", "%f[9]"] + ["%f[7]", "%f[6]"]
        out_format = "-F{}{}".format(infosep.join(tmp), tokensep) 
        tmp = ["%m"] + ["%f[{}]".format(i) for i in range(6)] + [""] * 5
        unk_format = "-U{}{}".format(infosep.join(tmp), tokensep) 
    else:
        tmp = ["%m"] + ["%f[{}]".format(i) for i in range(9)] + [""] * 2
        out_format = "-F{}{}".format(infosep.join(tmp), tokensep) 
        tmp = ["%m"] + ["%f[{}]".format(i) for i in range(7)] + [""] * 4
        unk_format = "-U{}{}".format(infosep.join(tmp), tokensep) 

    def _to_token(line):
        infos = line.split(infosep)
        if len(infos) < 2:
            # skip EOS line
            return None
        if len(infos) != 12:
            raise ValueError("Assume all lines have 12 elements, but got {} from {}".format(
                len(infos), line))

        infos = [None if i=="" else i for i in infos]
        if len(infos) == 12:
            return Token(*infos)
        raise ValueError()

    for doc in do_mecab_iter(x, "-E ", out_format, unk_format,
                             dictionary=dictionary, mecab_enc=mecab_enc):
        lines = doc.split(tokensep)
        tokens = [_to_token(line) for line in lines]
        tokens = [t for t in tokens if t is not None]
        if filter_func is not None:
            tokens = [t for t in tokens if filter_func(t)]
        if pos_filter is not None:
            pos_filter = set(pos_filter)
            tokens = [t for t in tokens if t.pos in pos_filter]
        if format_func is not None:
            tokens = [format_func(t) for t in tokens]
        yield tokens 

def mecab_batch(x, dictionary=None, mecab_enc=None, unidic_format=None,
                format_func=None, pos_filter=None, filter_func=None):
    return list(mecab_batch_iter(
        x, dictionary=dictionary, mecab_enc=mecab_enc, unidic_format=unidic_format,
        format_func=format_func, pos_filter=pos_filter, filter_func=filter_func))


def tokenize(x, mecab_enc=None, sysdic=None, userdic=None):
    """
    Tokenize a string 

    :param x:         unicode string
    :param mecab_enc: encoding mecab dictionary;
                      if None, automatically detected
    :param sysdic:    system dictionary directory
    :param userdic:   user dictionary file

    :return:    generator of tokens
    """
    
    # collect mecab options
    opts = []
    if sysdic is not None:
        opts += ['-d', sysdic]
    if userdic is not None:
        opts += ['-u', userdic]
        
    res = mecab_batch([x], *opts, mecab_enc=mecab_enc)[0]
    return res
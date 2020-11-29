# -*- coding: utf-8 -*-


import sys
from collections import namedtuple
from logging import getLogger
from .domecab import do_mecab, do_mecab_iter

logger = getLogger(__name__)

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
                     format_func=None, pos_filter=None, filter_func=None,
                     separators=None):
    """
    Tokenize a batch of strings

    :param x:              list of strings to parse
    :param mecab_enc:      encoding mecab dictionary;
                           if None, automatically detected
    :param dictionary:     system dictionary directory
                           folder name is allowed if it is in mecab's dicdir
    :param unidic_format:  bool indicating if the dictionary is in unidic format
    :param format_func:    function Token->Any to parse token
    :param pos_filter:     list of part-of-speeches to keep
    :param filter_func:    function Token->bool to filter tokens
    :param separators:     Strings or length 2. (token_sep, info_sep).
                           These should be strings that do not appear in data.
                           If None, automatically chosen from unicode upto 100

    :return:               generator of list of tokens
    """
    def _find_safe_separators(x, n=2):
        seps = []
        for i in range(1, 100):
            if len(seps) >= n:
                logger.debug("Chosen separators: %s (decimal code %s)",
                             seps[0:n], [ord(s) for s in seps])
                return seps[0:n]
            candidate = chr(i)
            flg = True
            for a in x:
                if a.find(candidate) >= 0:
                    flg = False
                    break
            if flg:
                seps.append(candidate)
        logger.error("Could not find a good separators")
        raise ValueError("Could not find a good separators." + \
                         "Please explicitly specify `separators=(tokensep, infosep)`.")
    if separators is None:
        tokensep, infosep = _find_safe_separators(x, n=2)
    else:
        tokensep, infosep = separators
    
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
                format_func=None, pos_filter=None, filter_func=None,
                separators=None):
    """
    Tokenize a batch of strings

    :param x:              list of strings to parse
    :param mecab_enc:      encoding mecab dictionary;
                           if None, automatically detected
    :param dictionary:     system dictionary directory
                           folder name is allowed if it is in mecab's dicdir
    :param unidic_format:  bool indicating if the dictionary is in unidic format
    :param format_func:    function Token->Any to parse token
    :param pos_filter:     list of part-of-speeches to keep
    :param filter_func:    function Token->bool to filter tokens
    :param separators:     Strings or length 2. (token_sep, info_sep).
                           These should be strings that do not appear in data.
                           If None, automatically chosen from unicode upto 100

    :return:               list of list of tokens
    """
    return list(mecab_batch_iter(
        x, dictionary=dictionary, mecab_enc=mecab_enc, unidic_format=unidic_format,
        format_func=format_func, pos_filter=pos_filter, filter_func=filter_func,
        separators=separators))


class MecabTokenizer:
    def __init__(self, dictionary=None, mecab_enc=None, unidic_format=None,
                 format_func=None, pos_filter=None, filter_func=None,
                 return_generator=False):
        self.dictionary = dictionary
        self.mecab_enc = mecab_enc
        self.unidic_format = unidic_format
        self.format_func = format_func
        self.pos_filter = pos_filter
        self.filter_func = filter_func
        self.return_generator = return_generator
    """
    Scikit-learn compatible tokenizer for a batch of strings

    :param mecab_enc:        encoding mecab dictionary;
                             if None, automatically detected
    :param dictionary:       system dictionary directory
                             folder name is allowed if it is in mecab's dicdir
    :param unidic_format:    bool indicating if the dictionary is in unidic format
    :param format_func:      function Token->Any to parse token
    :param pos_filter:       list of part-of-speeches to keep
    :param filter_func:      function Token->bool to filter tokens
    :param return_generator: bool indicating if transformer should return a generator
                             if false, returns a list
    """
    def fit_transform(self, X, y=None, **fit_params):
        return self.transform(X)
    
    def fit(self, X, y=None):
        # there is nothing to fit
        return self
    
    def transform(self, X):
        if self.return_generator:
            return mecab_batch_iter(X,
                                    dictionary=self.dictionary,
                                    mecab_enc=self.mecab_enc,
                                    unidic_format=self.unidic_format,
                                    format_func=self.format_func,
                                    pos_filter=self.pos_filter,
                                    filter_func=self.filter_func)
        else:
            return mecab_batch(X,
                               dictionary=self.dictionary,
                               mecab_enc=self.mecab_enc,
                               unidic_format=self.unidic_format,
                               format_func=self.format_func,
                               pos_filter=self.pos_filter,
                               filter_func=self.filter_func)

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
        
    res = mecab_batch([x], *opts, mecab_enc=mecab_enc)
    if len(res) > 0:
        return res[0]
    else:
        return []
# -*- coding: utf-8 -*-


import sys
from .domecab import do_mecab, do_mecab_iter


class Token:
    """
    Token type
    """

    def __init__(self, **kwargs):
        # note: variables are stored as unicode
        self.surface     = kwargs.pop('surface'    , None)
        self.pos         = kwargs.pop('pos'        , None)
        self.pos_detail1 = kwargs.pop('pos_detail1', None)
        self.pos_detail2 = kwargs.pop('pos_detail2', None)
        self.pos_detail3 = kwargs.pop('pos_detail3', None)
        self.infl_type   = kwargs.pop('infl_type'  , None)
        self.infl_form   = kwargs.pop('infl_form'  , None)
        self.base_form   = kwargs.pop('base_form'  , None)
        self.reading     = kwargs.pop('reading'    , None)
        self.phoenetic   = kwargs.pop('phoenetic'  , None)


    def __unicode__(self):
        tmp = [
            self.surface, 
            self.pos,
            self.pos_detail1,
            self.pos_detail2,
            self.pos_detail3,
            self.infl_type,
            self.infl_form,
            self.base_form,
            self.reading,
            self.phoenetic
        ]
        tmp = tuple(u'*' if a is None else a for a in tmp)
        
        out = u'%s\t%s,%s,%s,%s,%s,%s,%s,%s,%s' % tmp
        return out
    
    def __str__(self):
        """
        For python 3, returns unicode string
        For python 2, returns utf-8 encoded string
        To change the encoding, use `format`
        """
        out = self.__unicode__()
        if sys.version_info[0] == 2:
            out = out.encode('utf-8')
        return out
    
    def __format__(self, formatspec):
        """
        encode token info in an arbitrary encoding
        implemented for python 2 with 
        encoding other than utf8
        
        :param formatspec:  encoding
        """
        out = self.__unicode__()
        if sys.version_info[0] == 2:
            out = out.encode(formatspec)

        return out
        

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
        
    o = do_mecab(x, *opts, mecab_enc=mecab_enc)
    o = o.split('\n')
    for line in o:
        if line.strip()=="EOS":
            break
            
        # skip if the line contains not tab, which should separate the surface and info
        if line.find('\t') <= 0:
            continue
        # 表層形\t品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用型,活用形,原形,読み,発音
        surface, info = line.split("\t")
        info = info.split(",")
        info = [None if i == '*' else i for i in info]
        
        pos         = info[0] if len(info) > 0 else None
        pos_detail1 = info[1] if len(info) > 1 else None
        pos_detail2 = info[2] if len(info) > 2 else None
        pos_detail3 = info[3] if len(info) > 3 else None
        infl_type   = info[4] if len(info) > 4 else None
        infl_form   = info[5] if len(info) > 5 else None
        base_form   = info[6] if len(info) > 6 else None
        reading     = info[7] if len(info) > 7 else None
        phoenetic   = info[8] if len(info) > 8 else None
        
        token = Token(
            surface    =surface,
            pos        =pos,
            pos_detail1=pos_detail1,
            pos_detail2=pos_detail2,
            pos_detail3=pos_detail3,
            infl_type  =infl_type,
            infl_form  =infl_form,
            base_form  =base_form,
            reading    =reading,
            phoenetic  =phoenetic
        )
        yield token

    


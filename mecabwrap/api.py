# -*- coding: utf-8 -*-


from .domecab import do_mecab, do_mecab_iter


class Token:
    """
    Token type
    """

    def __init__(self, **kwargs):
        # 表層形\t品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用型,活用形,原形,読み,発音
        self.surface     = None
        self.pos         = None
        self.pos_detail1 = None
        self.pos_detail2 = None
        self.pos_detail3 = None
        self.infl_type   = None
        self.infl_form   = None
        self.base_form   = None
        self.reading     = None
        self.phoenetic   = None

        for key, value in kwargs.items():
            setattr(self, key, value)


    def __str__(self):
        tmp = [
            self.surface, 
            self.pos,
            self.pos_detail1,
            self.pos_detail2,
            self.infl_type,
            self.infl_form,
            self.base_form,
            self.reading,
            self.phoenetic
        ]
        tmp = tuple('*' if a is None else a for a in tmp)
        out = '%s\t%s,%s,%s,%s,%s,%s,%s,%s' % tmp
        return out


def tokenize(x):
    """
    Tokenize a string 

    :param x:   string

    :return:    generator of tokens
    """

    o = do_mecab(x).decode().split('\n')
    for line in o:
        if line.strip()=="EOS":
            break

        surface, info = line.split("\t")
        info = info.split(",")

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

    


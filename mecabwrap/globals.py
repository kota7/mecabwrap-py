# -*- coding: utf-8 -*-


__config = dict(
    mecab = "mecab"
)


def get_config(key):
    return __config[key]    


def set_config(key, val):
    __config[key] = val


def get_mecab():
    return get_config("mecab")


def set_mecab(val):
    set_config("mecab", val)




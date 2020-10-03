# -*- coding: utf-8 -*-


__config = dict(
    mecab = "mecab",
    mecab_config = "mecab-config"
)


def get_config(key):
    return __config[key]    


def set_config(key, val):
    __config[key] = val


def get_mecab():
    return get_config("mecab")


def set_mecab(val):
    set_config("mecab", val)


def get_mecab_config():
    return get_config("mecab_config")


def set_mecab_config(val):
    set_config("mecab_config", val)



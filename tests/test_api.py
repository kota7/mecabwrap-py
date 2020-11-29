#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import types
import sys
from mecabwrap.api import tokenize, str_token, mecab_batch, mecab_batch_iter, Token, MecabTokenizer


class TestTokenize(unittest.TestCase):
    def test_tokenize(self):
        tokens = tokenize(u'すもももももももものうち')
        words = [a.surface for a in tokens]
        self.assertEqual(
            words, 
            [u'すもも', u'も', u'もも', u'も', u'もも', u'の', u'うち']
         )

class TestBatch(unittest.TestCase):
    def test_batch(self):
        x = [u"明日は晴れるかな", u"雨なら読書をしよう"]
        y = mecab_batch(x)
        self.assertEqual(len(x), len(y))
        
        for a in y:
            self.assertEqual(type(a), list)
            for b in a:
                self.assertEqual(type(b), Token)
    
    def test_format(self):
        x = [u"明日は晴れるかな", u"雨なら読書をしよう"]
        y = mecab_batch(x, format_func=lambda x: x.surface)
        z = [[u"明日", u"は", u"晴れる", u"か", u"な"],
             [u"雨", u"なら", u"読書", u"を", u"しよ", u"う"]]
        for a, b in zip(y, z):
            for c, d in zip(a, b):
                self.assertEqual(c, d, msg=u"`{}` v `{}`".format(c, d))

    def test_filter(self):
        x = [u"明日は晴れるかな", u"雨なら読書をしよう"]
        y = mecab_batch(x, format_func=lambda x: x.surface,
                        pos_filter=(u"名詞", u"動詞"))
        z = [[u"明日", u"晴れる"],
             [u"雨", u"読書", u"しよ"]]
        for a, b in zip(y, z):
            for c, d in zip(a, b):
                self.assertEqual(c, d, msg=u"`{}` v `{}`".format(c, d))

        y = mecab_batch(x, format_func=lambda x: x.surface,
                        pos_filter=(u"名詞", u"動詞"),
                        filter_func=lambda x: len(x.surface)==2)
        z = [[u"明日"],
             [u"読書", u"しよ"]]
        for a, b in zip(y, z):
            for c, d in zip(a, b):
                self.assertEqual(c, d, msg=u"`{}` v `{}`".format(c, d))
                
    def test_batch_iter(self):
        x = [u"明日は晴れるかな", u"雨なら読書をしよう"]
        y = mecab_batch(x)
        z = mecab_batch_iter(x)
        self.assertEqual(type(z), types.GeneratorType)
        for a, b in zip(y, z): 
            self.assertEqual(len(a), len(b))
            for c, d in zip(a, b):
                self.assertEqual(c, d, msg=u"`{}` v `{}`".format(c, d))

    def test_tokenizer(self):
        x = [u"明日は晴れるかな", u"雨なら読書をしよう"]
        tokenizer = MecabTokenizer(format_func=lambda x: x.surface)
        y = tokenizer.transform(x)
        self.assertEqual(type(y), list)
        z = [[u"明日", u"は", u"晴れる", u"か", u"な"],
             [u"雨", u"なら", u"読書", u"を", u"しよ", u"う"]]
        for a, b in zip(y, z):
            for c, d in zip(a, b):
                self.assertEqual(c, d, msg=u"`{}` v `{}`".format(c, d))

        tokenizer = MecabTokenizer(format_func=lambda x: x.surface,
                                   return_generator=True)
        y = tokenizer.transform(x)
        self.assertEqual(type(y), types.GeneratorType)
        z = [[u"明日", u"は", u"晴れる", u"か", u"な"],
             [u"雨", u"なら", u"読書", u"を", u"しよ", u"う"]]
        for a, b in zip(y, z):
            for c, d in zip(a, b):
                self.assertEqual(c, d, msg=u"`{}` v `{}`".format(c, d))

    def test_auto_separators(self):
        x = [u"テスト" + chr(1) + u"です" + chr(2),
             chr(2) + u"文頭のケース",
             u"文末のケース" + chr(2),
             u"文中" + chr(1) + u"のケース"]
        y = mecab_batch(x)
        self.assertEqual(len(y), 4)

if __name__ == '__main__':
    unittest.main()
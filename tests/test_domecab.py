#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import re
from mecabwrap.domecab import do_mecab
from mecabwrap.domecab import do_mecab_iter


class TestDomecab(unittest.TestCase):
    def test_wakati(self):
        out = do_mecab('すもももももももものうち', '-Owakati').decode()
        self.assertEqual(out.strip(), 'すもも も もも も もも の うち')

    def test_default(self):
        out = do_mecab('メロンパンを食べる').decode()
        lbs = re.findall('\n', out) 
        self.assertEqual(len(lbs), 5)

        words = re.findall('\w+\t', out)
        words = [w[:-1] for w in words]
        self.assertEqual(words, ['メロン', 'パン', 'を', '食べる'])


class TestDomecabIter(unittest.TestCase):
    def test_iter(self):
        ins = ['となりの客はよく柿食う客だ', 'バスガス爆発']
        ct = 0
        for line in do_mecab_iter(ins, byline=False):
            ct += 1 
        self.assertEqual(ct, 2)

        ct = 0
        for line in do_mecab_iter(ins, '-Owakati', byline=True):
            ct += 1 
        self.assertEqual(ct, 2)

if __name__ == '__main__':
    unittest.main()



#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import re
from mecabwrap.domecab import do_mecab
from mecabwrap.domecab import do_mecab_vec
from mecabwrap.domecab import do_mecab_iter


class TestDomecab(unittest.TestCase):
    def test_wakati(self):
        out = do_mecab('すもももももももものうち', '-Owakati')
        self.assertEqual(out.strip(), 'すもも も もも も もも の うち')

    def test_default(self):
        out = do_mecab('メロンパンを食べる')
        lbs = re.findall('\n', out) 
        self.assertEqual(len(lbs), 5)

        words = re.findall('\w+\t', out)
        words = [w[:-1] for w in words]
        self.assertEqual(words, ['メロン', 'パン', 'を', '食べる'])


class TestDomecabVec(unittest.TestCase):
    def test_vec(self):
        ins = ['春はあけぼの', 'やうやう白くなりゆく山際']
        out = do_mecab_vec(ins, outpath=None)
        lbs = re.findall('\n', out)
        self.assertEqual(len(lbs), 10)

        words = re.findall('\w+\t', out)
        words = [w[:-1] for w in words]
        self.assertEqual(
            words,
            ['春', 'は', 'あけぼの', 'やうやう', 
             '白く', 'なり', 'ゆく', '山際']
        )

        lines = out.split('\n')
        lines = [line.strip() for line in lines]
        self.assertEqual(lines[3], 'EOS')
        self.assertEqual(lines[9], 'EOS')


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



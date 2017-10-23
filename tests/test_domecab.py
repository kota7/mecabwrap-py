#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import re
from mecabwrap.domecab import do_mecab
from mecabwrap.domecab import do_mecab_vec
from mecabwrap.domecab import do_mecab_iter


class TestDomecab(unittest.TestCase):
    def test_wakati(self):
        out = do_mecab(u'すもももももももものうち', '-Owakati')
        self.assertEqual(out.strip(), u'すもも も もも も もも の うち')

    def test_default(self):
        out = do_mecab(u'メロンパンを食べる')
        lbs = re.findall(r'\n', out) 
        self.assertEqual(len(lbs), 5)

        words = re.findall(r'[^\t\n]+\t', out)
        words = [w[:-1] for w in words]
        self.assertEqual(words, [u'メロン', u'パン', u'を', u'食べる'])


class TestDomecabVec(unittest.TestCase):
    def test_vec(self):
        ins = [u'春はあけぼの', u'やうやう白くなりゆく山際']
        out = do_mecab_vec(ins, outpath=None)
        lbs = re.findall(r'\n', out)
        self.assertEqual(len(lbs), 10)

        words = re.findall(r'[^\t\n]+\t', out)
        words = [w[:-1] for w in words]
        self.assertEqual(
            words,
            [u'春', u'は', u'あけぼの', u'やうやう', 
             u'白く', u'なり', u'ゆく', u'山際']
        )

        lines = out.split('\n')
        lines = [line.strip() for line in lines]
        self.assertEqual(lines[3], 'EOS')
        self.assertEqual(lines[9], 'EOS')


class TestDomecabIter(unittest.TestCase):
    def test_iter(self):
        ins = [u'となりの客はよく柿食う客だ', u'バスガス爆発']
        ct = 0
        for line in do_mecab_iter(ins, byline=False):
            ct += 1 
        self.assertEqual(ct, 2)

        ct = 0
        for line in do_mecab_iter(ins, '-Owakati', byline=True):
            ct += 1 
        self.assertEqual(ct, 2)



class TestMultipleOptions(unittest.TestCase):
    def test_multiple_options(self):
        out = do_mecab(u"すもももももももものうち", '-Bbegin\n', '-Eend\n')
        out = out.strip().split('\n')
        self.assertEqual(out[0] , 'begin')
        self.assertEqual(out[-1], 'end')

 
if __name__ == '__main__':
    unittest.main()



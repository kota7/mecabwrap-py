#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import re
import codecs
import types
from mecabwrap.domecab import do_mecab, do_mecab_vec, do_mecab_iter
from mecabwrap.utils import detect_mecab_enc


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
    
    def test_unicode(self):
        out = do_mecab(u'メロンパンを食べる', '-E', u'おわり\n', '-B', u'はじまり\n')
        words = re.findall(r'[^\t\n]+\t', out[1:-1])
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

    def test_linebreak(self):
        ins = [u'今日は\n赤ちゃん', u'私が\rママよ']
        out = do_mecab_vec(ins)
        eos = re.findall(r'EOS\n', out)
        self.assertEqual(len(eos), 2, out)

        out = do_mecab_vec(ins, '-Owakati')
        split = out.strip().split('\n')
        self.assertEqual(len(split), 2, out)


class TestDomecabIter(unittest.TestCase):

    def test_iter(self):
        ins = [u'アイスコーヒー', u'飲みたい']
        it = do_mecab_iter(ins, '-F%m\n', byline=True)
        self.assertTrue(isinstance(it, types.GeneratorType))
        self.assertEqual(
            list(it), [u'アイス', u'コーヒー', u'EOS', u'飲み', u'たい', u'EOS'])

        ins = [u'ぶどうパン', u'食べたい']
        it = do_mecab_iter(ins, '-F%m\n', byline=False)
        self.assertTrue(isinstance(it, types.GeneratorType))
        self.assertEqual(
            list(it), [u'ぶどう\nパン\nEOS', u'食べ\nたい\nEOS'])
            
    def test_iter_count(self):
        ins = [u'となりの客はよく柿食う客だ', u'バスガス爆発']
        ct = 0
        for line in do_mecab_iter(ins, byline=False):
            ct += 1 
        self.assertEqual(ct, 2)

        ct = 0
        for line in do_mecab_iter(ins, '-Owakati', byline=True):
            ct += 1 
        self.assertEqual(ct, 2)
        
        ct = 0
        for line in do_mecab_iter(ins, '-Owakati', byline=False):
            ct += 1 
        self.assertEqual(ct, 1)

    def test_iter_Eopt(self):
        ins = [u'となりの客はよく柿食う客だ', u'バスガス爆発']
        ct = 0
        for line in do_mecab_iter(ins, '-EEND\n', byline=False):
            ct += 1 
            self.assertEqual(line[-4:], '\nEND')
        self.assertEqual(ct, 2)

        ct = 0
        for line in do_mecab_iter(ins, '-E', 'END\n', byline=False):
            ct += 1 
            self.assertEqual(line[-4:], '\nEND')
        self.assertEqual(ct, 2)
        
        ct = 0
        for line in do_mecab_iter(ins, '--eos-format=END\n', byline=False):
            ct += 1 
            self.assertEqual(line[-4:], '\nEND')
        self.assertEqual(ct, 2)

        ct = 0
        for line in do_mecab_iter(ins, '--eos-format', 'END\n', byline=False):
            ct += 1 
            self.assertEqual(line[-4:], '\nEND')
        self.assertEqual(ct, 2)
    
    def test_iter_Eopt_unicode(self):    
        ins = [u'となりの客はよく柿食う客だ', u'バスガス爆発']
        ct = 0
        for line in do_mecab_iter(ins, u'-Eおしまい\n', byline=False):
            ct += 1 
            self.assertEqual(line[-5:], u'\nおしまい')
        self.assertEqual(ct, 2)

        ct = 0
        for line in do_mecab_iter(ins, '-E', u'おしまい\n', byline=False):
            ct += 1 
            self.assertEqual(line[-5:], u'\nおしまい')
        self.assertEqual(ct, 2)
        
        ct = 0
        for line in do_mecab_iter(ins, u'--eos-format=おしまい\n', byline=False):
            ct += 1 
            self.assertEqual(line[-5:], u'\nおしまい')
        self.assertEqual(ct, 2)

        ct = 0
        for line in do_mecab_iter(ins, '--eos-format', u'おしまい\n', byline=False):
            ct += 1 
            self.assertEqual(line[-5:], u'\nおしまい')
        self.assertEqual(ct, 2)

    def test_linebreak(self):
        ins = [u'今日は\n赤ちゃん', u'私が\rママよ']
        out = list(do_mecab_iter(ins, byline=False))
        self.assertEqual(len(out), 2, out)

        out = list(do_mecab_iter(ins, '-Owakati', byline=True))
        self.assertEqual(len(out), 2, out)
        

class TestMultipleOptions(unittest.TestCase):
    def test_multiple_options(self):
        out = do_mecab(u"すもももももももものうち", '-Bbegin\n', '-Eend\n')
        out = out.strip()
        out = re.split(r'(\r\n)|(\n)|(\r)', out)
        self.assertEqual(out[0], 'begin')
        self.assertEqual(out[-1], 'end')

 
if __name__ == '__main__':
    unittest.main()



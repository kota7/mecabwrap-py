#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import re
import codecs
import types
import warnings
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
        # vector element containing line break
        ins = [u'今日は\n赤ちゃん', u'私が\rママよ']
        out = do_mecab_vec(ins)
        eos = re.findall(r'EOS[\r]{0,1}\n', out)
        self.assertEqual(len(eos), 2, out)

        out = do_mecab_vec(ins, '-Owakati')
        split = out.strip().split('\n')
        self.assertEqual(len(split), 2, out)

    def test_large_input(self):
        enc = detect_mecab_enc()
        x = u'すもももももももものうち!'
        bx = len(x.encode(enc))
        # repeat this until it is over 20000 bytes
        tgt = 20000
        rep = int(tgt / bx + 1)
        y = x * rep  
        by = len(y.encode(enc))

        # make sure that the computation above works for all platform
        self.assertTrue(by > tgt)
        
        # option "auto" should set the input buffer size 
        # so entire string is regarded as a "sentense"
        out = do_mecab_vec([y], '-Owakati', buffer_size='auto')
        eos = re.findall(r'\n', out)
        self.assertEqual(len(eos), 1, 'length of out should equal 1')
        # make sure that entire strings are parsed by testing the
        # number of '!' is equal to rep
        num = re.findall(r'!', out)
        self.assertEqual(len(num), rep)

        # if we set the buffer size larger than the input, 
        # then we should get the same result as 'auto'
        out1 = do_mecab_vec([y], '-Owakati', buffer_size=by+1)
        out2 = do_mecab_vec([y], '-Owakati', buffer_size=by+2)
        self.assertEqual(out, out1)
        self.assertEqual(out, out2)
        
        # if we set the buffer size smaller or equal, 
        # we should get truncated outcome with a warning
        with warnings.catch_warnings(record=True) as w:
            out3 = do_mecab_vec([y], '-Owakati', buffer_size=by)
            self.assertEqual(len(w), 1)
        with warnings.catch_warnings(record=True) as w:
            out4 = do_mecab_vec([y], '-Owakati', buffer_size=by-1)
            self.assertEqual(len(w), 1)

        eos = re.findall(r'\n', out3)
        self.assertEqual(len(eos), 1, 'length of out3 should equal 1')
        eos = re.findall(r'\n', out4)
        self.assertEqual(len(eos), 1, 'length of out4 should equal 1')
        self.assertNotEqual(out, out3)
        self.assertNotEqual(out, out4)
        self.assertNotEqual(out3, out4)
        
        # if we don't set buffer size, then we will use the default value,
        # 8192. Since this is smaller than this input size, we expect warning,
        # but still outcome length is one, but truncated
        with warnings.catch_warnings(record=True) as w:
            out5 = do_mecab_vec([y], '-Owakati')
            self.assertEqual(len(w), 1)
        eos = re.findall(r'\n', out5)
        self.assertEqual(len(eos), 1, 'length of out5 should equal 1')
        self.assertNotEqual(out, out5)


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
        
    def test_large_input(self):
        enc = detect_mecab_enc()
        x = u'隣の客はよく柿食う客かな?'
        bx = len(x.encode(enc))
        # repeat this until it is over 30000 bytes
        tgt = 30000
        rep = int(tgt / bx + 1)
        y = x * rep  
        by = len(y.encode(enc))

        # make sure that the computation above works for all platform
        self.assertTrue(by > tgt)
        
        # option "auto" should set the input buffer size 
        # so entire string is regarded as a "sentense"
        out = do_mecab_iter([y], '-Owakati', byline=True, buffer_size='auto')
        out = list(out)
        self.assertEqual(len(out), 1, 'length of out should equal 1')
        # make sure that entire strings are parsed by testing the
        # number of '?' is equal to rep
        num = re.findall(r'\?', out[0])
        self.assertEqual(len(num), rep)

        # if we set the buffer size larger than the input, 
        # then we should get the same result as 'auto'
        out1 = do_mecab_iter([y], '-Owakati', byline=True, buffer_size=by+1)
        out1 = list(out1)
        out2 = do_mecab_iter([y], '-Owakati', byline=True, buffer_size=by+2)
        out2 = list(out2)
        self.assertEqual(out, out1)
        self.assertEqual(out, out2)
        
        # if we set the buffer size smaller or equal, 
        # we should get truncated outcome with a warning
        with warnings.catch_warnings(record=True) as w:
            out3 = do_mecab_iter([y], '-Owakati', byline=True, buffer_size=by)
            out3 = list(out3)
            self.assertEqual(len(w), 1)
        with warnings.catch_warnings(record=True) as w:
            out4 = do_mecab_iter([y], '-Owakati', byline=True, buffer_size=by-1)
            out4 = list(out4)
            self.assertEqual(len(w), 1)

        self.assertEqual(len(out3), 1, 'length of out3 should equal 1')
        self.assertEqual(len(out4), 1, 'length of out4 should equal 1')
        self.assertNotEqual(out, out3)
        self.assertNotEqual(out, out4)
        self.assertNotEqual(out3, out4)
        
        # if we don't set buffer size, then we will use the default value,
        # 8192. Since this is smaller than this input size, we expect warning,
        # but still outcome length is one, but truncated
        with warnings.catch_warnings(record=True) as w:
            out5 = do_mecab_iter([y], '-Owakati', byline=True)
            out5 = list(out5)
            self.assertEqual(len(w), 1)
        self.assertEqual(len(out), 1, 'length of out5 should equal 1')
        self.assertNotEqual(out, out5)


class TestMultipleOptions(unittest.TestCase):
    def test_multiple_options(self):
        out = do_mecab(u"すもももももももものうち", '-Bbegin\n', '-Eend\n')
        out = out.strip()
        out = re.split(r'(\r\n)|(\n)|(\r)', out)
        self.assertEqual(out[0], 'begin')
        self.assertEqual(out[-1], 'end')

 
if __name__ == '__main__':
    unittest.main()



#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
import re
import codecs
import tempfile
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
        
    def test_outfile_and_o(self):
        # generate filenames that do not exist
        path1 = tempfile.mktemp()
        path2 = tempfile.mktemp()
        path3 = tempfile.mktemp()
        # make sure they don't exist
        self.assertFalse(os.path.exists(path1))
        self.assertFalse(os.path.exists(path2))
        self.assertFalse(os.path.exists(path3))
        
        ret1 = do_mecab(u'赤巻紙青巻紙', outpath=path1)
        ret2 = do_mecab(u'赤巻紙青巻紙', '-o', path2)
        ret3 = do_mecab(u'赤巻紙青巻紙', '--output', path3)
        # confirm files are created 
        self.assertTrue(os.path.exists(path1))
        self.assertTrue(os.path.exists(path2))
        self.assertTrue(os.path.exists(path3))

        # confirm all results are empty
        self.assertEqual(ret1, u'')
        self.assertEqual(ret2, u'')
        self.assertEqual(ret3, u'')

        with open(path1, 'rb') as f:
            out1 = f.read()
        with open(path2, 'rb') as f:
            out2 = f.read()
        with open(path3, 'rb') as f:
            out3 = f.read()
        # confirm results are all identical
        self.assertEqual(out1, out2)
        self.assertEqual(out2, out3)

        enc = detect_mecab_enc()
        out = do_mecab(u'赤巻紙青巻紙')
        self.assertEqual(out, out1.decode(enc))
        self.assertTrue(len(out) > 0)

        # clean up
        os.remove(path1)
        os.remove(path2)
        os.remove(path3)
        # make sure they don't exist anymore
        self.assertFalse(os.path.exists(path1))
        self.assertFalse(os.path.exists(path2))
        self.assertFalse(os.path.exists(path3))

        # when both -o and outpath assigned
        # should get warning, and only outpath used
        with warnings.catch_warnings(record=True) as w:
            ret4 = do_mecab(u'赤巻紙青巻紙', '-o', path2, outpath=path1)
            self.assertEqual(len(w), 1) 
        self.assertTrue(os.path.exists(path1))
        self.assertFalse(os.path.exists(path2))
        with open(path1, 'rb') as f:
            out4 = f.read()
        self.assertEqual(out1, out4)


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
        

class TestLargeInput(unittest.TestCase):

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
        
        # test combination of (auto_buffer_size, truncate)
        # - True, True: correctly parsed 
        # - True, False: correctly parsed
        # - False, True: gets warning, result truncated
        # - False, False: gets warning, result has extra EOS
        out1 = do_mecab_vec([y], '-Owakati', auto_buffer_size=True, truncate=True)
        out2 = do_mecab_vec([y], '-Owakati', auto_buffer_size=True, truncate=False)
        with warnings.catch_warnings(record=True) as w:
            out3 = do_mecab_vec([y], '-Owakati', auto_buffer_size=False, truncate=True)
            self.assertEqual(len(w), 1, 'auto=False, trunc=True')
        with warnings.catch_warnings(record=True) as w:
            out4 = do_mecab_vec([y], '-Owakati', auto_buffer_size=False, truncate=False)
            self.assertEqual(len(w), 1, 'auto=False, trunc=False')

        # test of result length
        def num_eos(out): 
            return len(re.findall(r'\n', out))
        self.assertEqual(num_eos(out1), 1)
        self.assertEqual(num_eos(out2), 1)
        self.assertEqual(num_eos(out3), 1)
        self.assertTrue(num_eos(out4) > 1)

        # test of truncation
        def num_exclam(out):
            return len(re.findall(r'!', out))
        self.assertEqual(num_exclam(out1), rep)
        self.assertEqual(num_exclam(out2), rep)
        self.assertTrue(num_exclam(out3) < rep)
        #self.assertEqual(num_exclam(out4), rep)  
        # what happens with truncation is ambiguous

        # test of mannual -b option
        # if we set enough buffer size level, we should be fine
        out5 = do_mecab_vec([y], '-Owakati', '-b', str(by+1), 
                            auto_buffer_size=False, truncate=True)
        out6 = do_mecab_vec([y], '-Owakati', '-b', str(by+1), 
                            auto_buffer_size=False, truncate=False)
        self.assertEqual(num_eos(out5), 1)
        self.assertEqual(num_eos(out6), 1)
        self.assertEqual(num_exclam(out5), rep)
        self.assertEqual(num_exclam(out6), rep)

        # if the buffer size is small, we should get warning
        with warnings.catch_warnings(record=True) as w:
            out7 = do_mecab_vec([y], '-Owakati', '-b', str(by),
                                auto_buffer_size=False, truncate=True)
            self.assertEqual(len(w), 1, 'auto=False, trunc=True, -b small')
        with warnings.catch_warnings(record=True) as w:
            out8 = do_mecab_vec([y], '-Owakati', '-b', str(by),
                                auto_buffer_size=False, truncate=False)
            self.assertEqual(len(w), 1, 'auto=False, trunc=False, -b small')
        self.assertEqual(num_eos(out7), 1)
        self.assertTrue(num_eos(out8) > 1)
        self.assertTrue(num_exclam(out7) < rep)
        #self.assertEqual(num_exclam(out8), rep)  

        # if we set -b option and auto_buffer_size together,
        # we should get warning and we will use the auto size
        with warnings.catch_warnings(record=True) as w:
            out9 = do_mecab_vec([y], '-Owakati', '-b', str(by+100),
                                auto_buffer_size=True)
            self.assertEqual(len(w), 1, 'auto=False, trunc=False, -b small')
        self.assertEqual(num_eos(out9), 1)
        self.assertEqual(num_exclam(out7), rep)
        
        # result equality
        self.assertEqual(out1, out2)
        self.assertEqual(out1, out5)
        self.assertEqual(out1, out6)
        self.assertEqual(out1, out9)
        # and inequality
        self.assertNotEqual(out1, out3)
        self.assertNotEqual(out1, out4)
        self.assertNotEqual(out1, out7)
        self.assertNotEqual(out1, out8)

    def test_large_input_iter(self):
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
        
        out1 = do_mecab_iter(
            [y], '-Owakati', byline=True, auto_buffer_size=True, truncate=True)
        out1 = list(out1)
        out2 = do_mecab_iter(
            [y], '-Owakati', byline=True, auto_buffer_size=True, truncate=False)
        out2 = list(out2)

class TestMultipleOptions(unittest.TestCase):
    def test_multiple_options(self):
        out = do_mecab(u"すもももももももものうち", '-Bbegin\n', '-Eend\n')
        out = out.strip()
        out = re.split(r'(\r\n)|(\n)|(\r)', out)
        self.assertEqual(out[0], 'begin')
        self.assertEqual(out[-1], 'end')

 
if __name__ == '__main__':
    unittest.main()



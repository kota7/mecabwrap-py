#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from mecabwrap.utils import *


class TestMecabOption(unittest.TestCase):
    def test_opt(self):
        args = ['-d', 'foo', 
                '--output-format-type=wakati', 
                '--eos-format', 'END',
                '-p', '--dump-config']  

        ret = get_mecab_opt('-d', *args)
        self.assertEqual(ret, 'foo')
        ret = get_mecab_opt('--dicdir', *args)
        self.assertEqual(ret, 'foo')

        ret = get_mecab_opt('-O', *args)
        self.assertEqual(ret, 'wakati')
        ret = get_mecab_opt('--output-format-type', *args)
        self.assertEqual(ret, 'wakati')

        ret = get_mecab_opt('-E', *args)
        self.assertEqual(ret, 'END')
        ret = get_mecab_opt('--eos-format', *args)
        self.assertEqual(ret, 'END')

        ret = get_mecab_opt('-N', *args)
        self.assertTrue(ret is None)
        ret = get_mecab_opt('--nbest', *args)
        self.assertTrue(ret is None)

        ret = get_mecab_opt('-t', *args)
        self.assertTrue(ret is None)
        ret = get_mecab_opt('--theta', *args)
        self.assertTrue(ret is None)

        ret = get_mecab_opt('-p', *args)
        self.assertTrue(ret)
        ret = get_mecab_opt('--partial', *args)
        self.assertTrue(ret)

        ret = get_mecab_opt('-P', *args)
        self.assertTrue(ret)
        ret = get_mecab_opt('--dump-config', *args)
        self.assertTrue(ret)

        ret = get_mecab_opt('-m', *args)
        self.assertFalse(ret)
        ret = get_mecab_opt('--marginal', *args)
        self.assertFalse(ret)


if __name__ == '__main__':
    unittest.main()

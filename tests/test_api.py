#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import sys
from mecabwrap.api import tokenize, str_token


class TestTokenize(unittest.TestCase):
    def test_tokenize(self):
        tokens = tokenize(u'すもももももももものうち')
        words = [a.surface for a in tokens]
        self.assertEqual(
            words, 
            [u'すもも', u'も', u'もも', u'も', u'もも', u'の', u'うち']
         )

    def test_print_str(self):
        """
        print(token) should give str in both in python2 and 3
        """
        tokens = tokenize(u'すもももももももものうち')
        for token in tokens:
            s = str_token(token)
            self.assertTrue(isinstance(s, str))


if __name__ == '__main__':
    unittest.main()
       



#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import sys
from mecabwrap.api import tokenize


class TestTokenize(unittest.TestCase):
    def test_tokenize(self):
        tokens = tokenize(u'すもももももももものうち')
        words = [a.surface for a in tokens]
        self.assertEqual(
            words, 
            [u'すもも', u'も', u'もも', u'も', u'もも', u'の', u'うち']
        )
    
    def test_print_unicode(self):
        """
        print(token) should print unicode string
        """
        tokens = tokenize(u'すもももももももものうち')
        for token in tokens:
            s = token.__str__()
            if sys.version_info[0] == 2:
                self.assertTrue(isinstance(s, unicode))
            else:
                self.assertTrue(isinstance(s, str))

    def test_format_str(self):
        """
        format(token) should give str in both in python2 and 3
        """
        tokens = tokenize(u'すもももももももものうち')
        for token in tokens:
            s = token.__format__('utf-8')
            self.assertTrue(isinstance(s, str))

         



if __name__ == '__main__':
    unittest.main()
       



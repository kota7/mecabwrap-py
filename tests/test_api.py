#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from mecabwrap.api import tokenize


class TestTokenize(unittest.TestCase):
    def test_tokenize(self):
        tokens = tokenize('すもももももももものうち')
        words = [a.surface for a in tokens]
        self.assertEqual(
            words, 
            ['すもも', 'も', 'もも', 'も', 'もも', 'の', 'うち']
        )



if __name__ == '__main__':
    unittest.main()
       



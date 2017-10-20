#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import re
from mecabwrap.domecab import do_mecab


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


if __name__ == '__main__':
    unittest.main()



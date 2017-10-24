#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from mecabwrap.utils import get_mecab_enc


class TestTokenize(unittest.TestCase):
    def test_detect_enc(self):
        enc = get_mecab_enc()
        # make sure that encode + decode works
        s = u'あいうえお'
        self.assertEqual(s.encode(enc).decode(enc), s)
        


if __name__ == '__main__':
    unittest.main()
       



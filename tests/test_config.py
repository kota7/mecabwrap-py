#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest
from mecabwrap import tokenize
from mecabwrap.config import set_mecab
from mecabwrap.config import get_mecab


class TestSetGet(unittest.TestCase):
    """
    confirm that `set` changes the `get` result 
    """
    def test_set_and_get(self):
        set_mecab("foo")
        self.assertEqual(get_mecab(), "foo")
        set_mecab("bar")
        self.assertEqual(get_mecab(), "bar")

        set_mecab("mecab")



if __name__ == '__main__':
    unittest.main()

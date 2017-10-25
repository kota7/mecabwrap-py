#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest
import subprocess
from mecabwrap import tokenize, do_mecab, do_mecab_vec, do_mecab_iter
from mecabwrap.config import set_mecab, get_mecab
from mecabwrap.utils import mecab_exists

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

class TestNoMeCab(unittest.TestCase):
    """
    set `mecab` to a random command and
    check the behavior of the functions
    """
    
    def test_no_mecab(self):        
        # find a command that does not exist
        command = 'mecabb'
        while True:
            try: 
                p = subprocess.Popen([command])
            except IOError:
                break
            command += 'b'
        
        
        # set mecab to the invalid command
        set_mecab(command)
        self.assertFalse(mecab_exists())
    
        # tokenize should be contain no element
        o = list(tokenize(u'すもももももももものうち'))
        self.assertEqual(len(o), 0)
    
        # do_mecab should return an empty string
        o = do_mecab(u'すもももももももものうち')
        self.assertEqual(o, u'')
    
        # do_mecab_vec should also return an empty string
        o = do_mecab_vec(u'すもももももももものうち')
        self.assertEqual(o, u'')
    
        # do_mecab_iter should contain no element
        o = list(do_mecab_iter(u'すもももももももものうち'))
        self.assertEqual(len(o), 0)
        
        # put back mecab
        set_mecab('mecab')
        self.assertTrue(mecab_exists())
        
if __name__ == '__main__':
    unittest.main()


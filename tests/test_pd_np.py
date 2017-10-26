#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import re
import sys
from mecabwrap.domecab import do_mecab_vec
import numpy as np

# pandas import may fail with python 2.6 due to
# 'cannot import name OrderedDict' or similar
# skip pandas test for python 2.6 or lower
PY26 = sys.version_info[0] == 2 and sys.version_info[0] <= 6
if not PY26:
    import pandas as pd


class TestPdNp(unittest.TestCase):
    def test_pandas(self):
        if PY26:
            return
            
        x1 = [u'会いたくて', u'会いたくて', u'震える']
        x2 = pd.Series(x1)
        
        o1 = do_mecab_vec(x1)
        o2 = do_mecab_vec(x2)
        self.assertEqual(o1, o2)

    def test_numpy(self):
        x1 = [u'会いたくて', u'会いたくて', u'震える']
        x2 = np.array(x1)
        
        o1 = do_mecab_vec(x1)
        o2 = do_mecab_vec(x2)
        self.assertEqual(o1, o2)
 
 
if __name__ == '__main__':
    unittest.main()



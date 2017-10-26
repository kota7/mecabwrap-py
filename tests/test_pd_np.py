#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import re
import numpy as np
import pandas as pd
from mecabwrap.domecab import do_mecab_vec


class TestPdNp(unittest.TestCase):
    def test_pandas(self):
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



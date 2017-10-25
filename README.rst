
mecabwrap
=========

|Build Status|

**mecabwrap** is yet another Python interface to `MeCab Morphological
Analyzer <http://taku910.github.io/mecab/>`__.

It is designed to work seamlessly on Unix and Windows machine.

Requirement
-----------

-  Python 2.6+ or 3.3+
-  MeCab 0.996

Installation
------------

1. Install MeCab
~~~~~~~~~~~~~~~~

**Ubuntu**

.. code:: bash

    $ sudo apt-get install mecab libmecab-dev mecab-ipadic-utf8

**Mac OSX**

.. code:: bash

    $ brew install mecab mecab-ipadic

**Windows**

Download and run the
`installer <https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7WElGUGt6ejlpVXc>`__.

See also: `official website <http://taku910.github.io/mecab/#install>`__

2. Install this Package
~~~~~~~~~~~~~~~~~~~~~~~

Install from PyPI

.. code:: bash

    $ pip install mecabwrap
    
or, from GitHub

.. code:: bash

    $ git clone --depth 1 https://github.com/kota7/mecabwrap-py.git
    $ cd mecabwrap-py
    $ pip install -U .

Quick Check
-----------

To verify that the MeCab has been sucessfully,

.. code:: bash

    $ mecab -v
    # should result in `mecab of 0.996` or similar.

If this causes error or gives an unexpected outcome, then it is either MeCab has not been installed or MeCab is not
on the search path.

The code below verifies that MeCab works properly.

.. code:: bash

    $ echo すもももももももものうち | mecab
    # すもも   名詞,一般,*,*,*,*,すもも,スモモ,スモモ
    # も 助詞,係助詞,*,*,*,*,も,モ,モ
    # もも    名詞,一般,*,*,*,*,もも,モモ,モモ
    # も 助詞,係助詞,*,*,*,*,も,モ,モ
    # もも    名詞,一般,*,*,*,*,もも,モモ,モモ
    # の 助詞,連体化,*,*,*,*,の,ノ,ノ
    # うち    名詞,非自立,副詞可能,*,*,*,うち,ウチ,ウチ


Finally, to verify that the package is success fully installed,

.. code:: bash

    $ python

.. code:: python

    >>> from mecabwrap import tokenize
    >>> for token in tokenize(u"すもももももももものうち"): 
    ...     print(token)
    ... 
    すもも	名詞,一般,*,*,*,*,すもも,スモモ,スモモ
    も	助詞,係助詞,*,*,*,*,も,モ,モ
    もも	名詞,一般,*,*,*,*,もも,モモ,モモ
    も	助詞,係助詞,*,*,*,*,も,モ,モ
    もも	名詞,一般,*,*,*,*,もも,モモ,モモ
    の	助詞,連体化,*,*,*,*,の,ノ,ノ
    うち	名詞,非自立,副詞可能,*,*,*,うち,ウチ,ウチ


.. |Build Status| image:: https://travis-ci.org/kota7/mecabwrap-py.svg?branch=master
   :target: https://travis-ci.org/kota7/mecabwrap-py



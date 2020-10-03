

mecabwrap
=========

.. image:: https://travis-ci.org/kota7/mecabwrap-py.svg?branch=master
    :target: https://travis-ci.org/kota7/mecabwrap-py
.. image:: https://ci.appveyor.com/api/projects/status/oidn1rfte6u8kavs/branch/master?svg=true
    :target: https://ci.appveyor.com/project/kota7/mecabwrap-py/branch/master
.. image:: https://badge.fury.io/py/mecabwrap.svg
    :target: https://badge.fury.io/py/mecabwrap

**mecabwrap** is yet another Python interface to `MeCab Morphological
Analyzer <http://taku910.github.io/mecab/>`__.

Its goal is to provide intuitive APIs that work on Unix and Windows machines seamlessly.

Requirement
-----------

-  Python 2.7+ or 3.4+ (May also work on older versions)
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

Following command will print the MeCab version. Otherwise, you do not
have MeCab installed or MeCab is not on the search path.

.. code:: bash

    $ mecab -v
    # should print `mecab of 0.996` or similar.


To verify that the package is successfully installed, try the following:

.. code:: bash

    $ python

.. code:: python

    >>> from mecabwrap import tokenize
    >>> for token in tokenize(u"すもももももももものうち"): 
    ...     print(token)
    ... 
    すもも 名詞,一般,*,*,*,*,すもも,スモモ,スモモ
    も   助詞,係助詞,*,*,*,*,も,モ,モ
    もも  名詞,一般,*,*,*,*,もも,モモ,モモ
    も   助詞,係助詞,*,*,*,*,も,モ,モ
    もも  名詞,一般,*,*,*,*,もも,モモ,モモ
    の   助詞,連体化,*,*,*,*,の,ノ,ノ
    うち  名詞,非自立,副詞可能,*,*,*,うち,ウチ,ウチ


Usage
-----

Visit the `example page <https://nbviewer.jupyter.org/github/kota7/mecabwrap-py/blob/master/notebook/mecabwrap%20-%20Python%20Interface%20to%20MeCab%20for%20Unix%20and%20Windows.ipynb>`__ for more detail.

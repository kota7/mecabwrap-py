
# mecabwrap

[![Build Status](https://travis-ci.org/kota7/mecabwrap-py.svg?branch=master)](https://travis-ci.org/kota7/mecabwrap-py)

**mecabwrap** is yet another wrapper for [MeCab Morphological Analyzer](http://taku910.github.io/mecab/).

It is designed to work seamlessly on Unix and Windows machine.


## Requirement

- Python 2.6+ or 3.4+
- MeCab 0.996


## Installation


### 1. Install MeCab

**Ubuntu**

```bash
$ sudo apt-get install mecab libmecab-dev mecab-ipadic-utf8
```

**Mac OSX**

```bash
$ sudo apt-get install mecab libmecab-dev mecab-ipadic-utf8
```

**Windows**

Download and run the [installer](https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7WElGUGt6ejlpVXc).

See also: [official website](http://taku910.github.io/mecab/#install) 



### 2. Install this Package

```bash
$ git clone --depth 1 https://github.com/kota7/mecabwrap-py.git
$ cd mecabwrap-py
$ pip install .U
```


## Quick Check


Verify that the MeCab has been sucessfully installed by:

```bash
$ mecab -v
# should result in `mecab of 0.996` or similar.
```

Otherwise, you do not have MeCab installed successfully or MeCab is not on the search path.


```bash
$ echo すもももももももものうち | mecab
# すもも	名詞,一般,*,*,*,*,すもも,スモモ,スモモ
# も	助詞,係助詞,*,*,*,*,も,モ,モ
# もも	名詞,一般,*,*,*,*,もも,モモ,モモ
# も	助詞,係助詞,*,*,*,*,も,モ,モ
# もも	名詞,一般,*,*,*,*,もも,モモ,モモ
# の	助詞,連体化,*,*,*,*,の,ノ,ノ
# うち	名詞,非自立,副詞可能,*,*,*,うち,ウチ,ウチ
```


To verify that the package if success fully installed,

```bash
$ python
```

```python
>>> from mecabwrap import tokenize
>>> for token in tokenize(u"すもももももももものうち"): 
...     print(token)
... 
すもも	名詞,*,*,*,*,すもも,スモモ,スモモ
も	助詞,*,*,*,*,も,モ,モ
もも	名詞,*,*,*,*,もも,モモ,モモ
も	助詞,*,*,*,*,も,モ,モ
もも	名詞,*,*,*,*,もも,モモ,モモ
の	助詞,*,*,*,*,の,ノ,ノ
うち	名詞,*,*,*,*,うち,ウチ,ウチ
```






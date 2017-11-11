
# mecabwrap


**mecabwrap** is yet another Python interface to [MeCab Morphological Analyzer](http://taku910.github.io/mecab/).

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
すもも	名詞,一般,*,*,*,*,すもも,スモモ,スモモ
も	助詞,係助詞,*,*,*,*,も,モ,モ
もも	名詞,一般,*,*,*,*,もも,モモ,モモ
も	助詞,係助詞,*,*,*,*,も,モ,モ
もも	名詞,一般,*,*,*,*,もも,モモ,モモ
の	助詞,連体化,*,*,*,*,の,ノ,ノ
うち	名詞,非自立,副詞可能,*,*,*,うち,ウチ,ウチ
```



## Usage


### A Simple Tokenizer

The `tokenize` function is a high level API for splitting a text into tokens.
It returns a generator of tokens.


```python
from mecabwrap import tokenize

for token in tokenize('すもももももももものうち'):
    print(token)
```

    すもも	名詞,一般,*,*,*,*,すもも,スモモ,スモモ
    も	助詞,係助詞,*,*,*,*,も,モ,モ
    もも	名詞,一般,*,*,*,*,もも,モモ,モモ
    も	助詞,係助詞,*,*,*,*,も,モ,モ
    もも	名詞,一般,*,*,*,*,もも,モモ,モモ
    の	助詞,連体化,*,*,*,*,の,ノ,ノ
    うち	名詞,非自立,副詞可能,*,*,*,うち,ウチ,ウチ


### Using MeCab Options

To configure the MeCab calls, one may use `do_` functions that support arbitrary number of MeCab options.  
Currently, the following three `do_` functions are provided.
- `do_mecab`: works with a single input text.
- `do_mecab_vec`: works with a multiple input texts.
- `do_mecab_iter`: works with a multiple input texts and returns a generator.

For example, following code invokes the *wakati* option, so the outcome be words separated by spaces with no meta information. 
See [the official site](http://taku910.github.io/mecab/format.html) for more details.


```python
from mecabwrap import do_mecab
out = do_mecab('人生楽ありゃ苦もあるさ', '-Owakati')
print(out)
```

    人生 楽 ありゃ 苦 も ある さ 
    


The exapmle below uses `do_mecab_vec` to parse multiple texts.
Note that `-F` option configures the outcome formatting.



```python
from mecabwrap import do_mecab_vec
ins = ['春はあけぼの', 'やうやう白くなりゆく山際', '少し明かりて', '紫だちたる雲の細くたなびきたる']

out = do_mecab_vec(ins, '-F%f[6](%f[1]) | ')
print(out)
```

    春(一般) | は(係助詞) | あけぼの(固有名詞) | EOS
    やうやう(一般) | 白い(自立) | なる(自立) | ゆく(非自立) | 山際(一般) | EOS
    少し(助詞類接続) | 明かり(一般) | て(格助詞) | EOS
    紫(一般) | だ() | ちる(自立) | たり() | 雲(一般) | の(連体化) | 細い(自立) | たなびく(自立) | たり() | EOS
    


### Returning Iterators

When the number of input text is large, then holding the outcomes in the memory may not be a good idea.  `do_mecab_iter` function, which works for multiple texts, returns a generator of MeCab results.
When `byline=True`, each chunk is a line, which corresponds to a token in the default setting.
When `byline=False`, each chunk is a document, where a document is assumed to terminate with `'EOS'.`


```python
from mecabwrap import do_mecab_iter

ins = ['春はあけぼの', 'やうやう白くなりゆく山際', '少し明かりて', '紫だちたる雲の細くたなびきたる']

i = 0
for text in do_mecab_iter(ins, byline=False):
    i += 1
    print('---(' + str(i) + ')\n' + text)
```

    ---(1)
    春	名詞,一般,*,*,*,*,春,ハル,ハル
    は	助詞,係助詞,*,*,*,*,は,ハ,ワ
    あけぼの	名詞,固有名詞,地域,一般,*,*,あけぼの,アケボノ,アケボノ
    EOS
    ---(2)
    やうやう	副詞,一般,*,*,*,*,やうやう,ヤウヤウ,ヨーヨー
    白く	形容詞,自立,*,*,形容詞・アウオ段,連用テ接続,白い,シロク,シロク
    なり	動詞,自立,*,*,五段・ラ行,連用形,なる,ナリ,ナリ
    ゆく	動詞,非自立,*,*,五段・カ行促音便ユク,基本形,ゆく,ユク,ユク
    山際	名詞,一般,*,*,*,*,山際,ヤマギワ,ヤマギワ
    EOS
    ---(3)
    少し	副詞,助詞類接続,*,*,*,*,少し,スコシ,スコシ
    明かり	名詞,一般,*,*,*,*,明かり,アカリ,アカリ
    て	助詞,格助詞,連語,*,*,*,て,テ,テ
    EOS
    ---(4)
    紫	名詞,一般,*,*,*,*,紫,ムラサキ,ムラサキ
    だ	助動詞,*,*,*,特殊・ダ,基本形,だ,ダ,ダ
    ち	動詞,自立,*,*,五段・ラ行,体言接続特殊２,ちる,チ,チ
    たる	助動詞,*,*,*,文語・ナリ,体言接続,たり,タル,タル
    雲	名詞,一般,*,*,*,*,雲,クモ,クモ
    の	助詞,連体化,*,*,*,*,の,ノ,ノ
    細く	形容詞,自立,*,*,形容詞・アウオ段,連用テ接続,細い,ホソク,ホソク
    たなびき	動詞,自立,*,*,五段・カ行イ音便,連用形,たなびく,タナビキ,タナビキ
    たる	助動詞,*,*,*,文語・ナリ,体言接続,たり,タル,タル
    EOS


### Writing the outcome to file

To write the MeCab outcomes directly to a file, one may either use `-o` option or `outpath` argument.  Note that this does not work with `do_mecab_iter`, since it is designed to write the outcomes to a temporary file.



```python
do_mecab('すもももももももものうち', '-osumomo1.txt')
# or,
do_mecab('すもももももももものうち', outpath='sumomo2.txt')

with open('sumomo1.txt') as f: 
    print(f.read())
with open('sumomo2.txt') as f: 
    print(f.read())

import os
# clean up
os.remove('sumomo1.txt')
os.remove('sumomo2.txt')

# this does not create a file
do_mecab_iter(['すもももももももものうち'], '-osumomo3.txt')
os.path.exists('sumomo3.txt')
```

    すもも	名詞,一般,*,*,*,*,すもも,スモモ,スモモ
    も	助詞,係助詞,*,*,*,*,も,モ,モ
    もも	名詞,一般,*,*,*,*,もも,モモ,モモ
    も	助詞,係助詞,*,*,*,*,も,モ,モ
    もも	名詞,一般,*,*,*,*,もも,モモ,モモ
    の	助詞,連体化,*,*,*,*,の,ノ,ノ
    うち	名詞,非自立,副詞可能,*,*,*,うち,ウチ,ウチ
    EOS
    
    すもも	名詞,一般,*,*,*,*,すもも,スモモ,スモモ
    も	助詞,係助詞,*,*,*,*,も,モ,モ
    もも	名詞,一般,*,*,*,*,もも,モモ,モモ
    も	助詞,係助詞,*,*,*,*,も,モ,モ
    もも	名詞,一般,*,*,*,*,もも,モモ,モモ
    の	助詞,連体化,*,*,*,*,の,ノ,ノ
    うち	名詞,非自立,副詞可能,*,*,*,うち,ウチ,ウチ
    EOS
    





    False



### Note on Python 2

All text inputs are assumed to be unicode.  
In Python2, inputs must be `u''` string, not `''`.
In python3, `str` type is unicode, so `u''` and `''` are equivalent.


```python
o1 = do_mecab('すもももももももものうち')   # this works only for python 3
o2 = do_mecab(u'すもももももももものうち')  # this works both for python 2 and 3
print(o1)
print(o2)
```

    すもも	名詞,一般,*,*,*,*,すもも,スモモ,スモモ
    も	助詞,係助詞,*,*,*,*,も,モ,モ
    もも	名詞,一般,*,*,*,*,もも,モモ,モモ
    も	助詞,係助詞,*,*,*,*,も,モ,モ
    もも	名詞,一般,*,*,*,*,もも,モモ,モモ
    の	助詞,連体化,*,*,*,*,の,ノ,ノ
    うち	名詞,非自立,副詞可能,*,*,*,うち,ウチ,ウチ
    EOS
    
    すもも	名詞,一般,*,*,*,*,すもも,スモモ,スモモ
    も	助詞,係助詞,*,*,*,*,も,モ,モ
    もも	名詞,一般,*,*,*,*,もも,モモ,モモ
    も	助詞,係助詞,*,*,*,*,も,モ,モ
    もも	名詞,一般,*,*,*,*,もも,モモ,モモ
    の	助詞,連体化,*,*,*,*,の,ノ,ノ
    うち	名詞,非自立,副詞可能,*,*,*,うち,ウチ,ウチ
    EOS
    


### Note on dictionary encodings

The functions takes `mecab_enc` option, which indicates the encoding of the MeCab dictionary being used.  Usually this can be left as the default value `None`, so that the encoding is automatically detected.  Alternatively, one may specify the encoding explicitly.


```python
o1 = do_mecab('日本列島改造論', mecab_enc=None)      # default
print(o1)

o2 = do_mecab('日本列島改造論', mecab_enc='utf-8')   # explicitly specified
print(o2)

#o3 = do_mecab('日本列島改造論', mecab_enc='cp932')   # wrong encoding, fails

```

    日本	名詞,固有名詞,地域,国,*,*,日本,ニッポン,ニッポン
    列島	名詞,一般,*,*,*,*,列島,レットウ,レットー
    改造	名詞,サ変接続,*,*,*,*,改造,カイゾウ,カイゾー
    論	名詞,接尾,一般,*,*,*,論,ロン,ロン
    EOS
    
    日本	名詞,固有名詞,地域,国,*,*,日本,ニッポン,ニッポン
    列島	名詞,一般,*,*,*,*,列島,レットウ,レットー
    改造	名詞,サ変接続,*,*,*,*,改造,カイゾウ,カイゾー
    論	名詞,接尾,一般,*,*,*,論,ロン,ロン
    EOS
    


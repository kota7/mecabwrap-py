
# mecabwrap


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



## Usage


### A Simple Tokenizer

The `tokenize` function provides a high level API for splitting a text into tokens.
It returns a generator of tokens.


```python
from mecabwrap import tokenize

for token in tokenize('すもももももももものうち'):
    print(token)
```

    すもも	名詞,一般,*,*,*,すもも,スモモ,スモモ
    も	助詞,係助詞,*,*,*,も,モ,モ
    もも	名詞,一般,*,*,*,もも,モモ,モモ
    も	助詞,係助詞,*,*,*,も,モ,モ
    もも	名詞,一般,*,*,*,もも,モモ,モモ
    の	助詞,連体化,*,*,*,の,ノ,ノ
    うち	名詞,非自立,副詞可能,*,*,うち,ウチ,ウチ


### Multiple Inputs

With more than on text inputs, `do_mecab_iter` function returns a generator of MeCab results.
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


### Using MeCab Options

The `do_` functions supports options of MeCab.  For example, following code invokes the *wakati* option, so the outcome be words separated by spaces with no meta information. 
Note that `byline` is set to `False`, since with the *wakati* option each line represents a text and `"EOS"` marker is not used.


```python
ins = ['春はあけぼの', 'やうやう白くなりゆく山際', '少し明かりて', '紫だちたる雲の細くたなびきたる']

for text in do_mecab_iter(ins, '-Owakati', byline=True):
    print(text)
```

    春 は あけぼの
    やうやう 白く なり ゆく 山際
    少し 明かり て
    紫 だ ち たる 雲 の 細く たなびき たる


More complex output formatting is allowed with `-F` option.  
See [the official site](http://taku910.github.io/mecab/format.html) for more details.


```python
ins = ['春はあけぼの', 'やうやう白くなりゆく山際', '少し明かりて', '紫だちたる雲の細くたなびきたる']

for text in do_mecab_iter(ins, '-F%f[6](%f[1]) | ', byline=True):
    print(text)
```

    春(一般) | は(係助詞) | あけぼの(固有名詞) | EOS
    やうやう(一般) | 白い(自立) | なる(自立) | ゆく(非自立) | 山際(一般) | EOS
    少し(助詞類接続) | 明かり(一般) | て(格助詞) | EOS
    紫(一般) | だ() | ちる(自立) | たり() | 雲(一般) | の(連体化) | 細い(自立) | たなびく(自立) | たり() | EOS


### Note

- `-o` option (output file) does not work with `do_mecab_iter`, since it is designed to write the outcomes to a temporary file.
- To write the outcome directly to a file, use `do_mecab` or `do_mecab_vec` with `outpath` argument.




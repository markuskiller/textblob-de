textblob-de README
==================

[![textblob\_de - latest PyPI version](https://img.shields.io/pypi/v/textblob-de.svg)](https://pypi.python.org/pypi/textblob-de/)
[![Travis-CI](https://travis-ci.org/markuskiller/textblob-de.png?branch=dev)](https://travis-ci.org/markuskiller/textblob-de)
[![Documentation Status](https://readthedocs.org/projects/textblob-de/badge/?version=latest)](http://textblob-de.readthedocs.org/en/latest/)
[![Number of PyPI downloads](https://img.shields.io/pypi/dm/textblob-de.svg)](https://pypi.python.org/pypi/textblob-de/)
[![LICENSE info](https://img.shields.io/github/license/markuskiller/textblob-de.svg)](http://choosealicense.com/licenses/mit/)

German language support for
[TextBlob](http://textblob.readthedocs.org/en/dev/) by Steven Loria.

This python package is being developed as a `TextBlob` **Language
Extension**. See [Extension
Guidelines](https://textblob.readthedocs.org/en/dev/contributing.html)
for details.

Features
--------

-   **NEW:** Works with Python3.7
-   All directly accessible `textblob_de` classes (e.g. `Sentence()` or
    `Word()`) are initialized with default models for German
-   Properties or methods that do not yet work for German raise a
    `NotImplementedError`
-   German sentence boundary detection and tokenization
    (`NLTKPunktTokenizer`)
-   Consistent use of specified tokenizer for all tools
    (`NLTKPunktTokenizer` or `PatternTokenizer`)
-   Part-of-speech tagging (`PatternTagger`) with keyword
    `include_punc=True` (defaults to `False`)
-   Tagset conversion in `PatternTagger` with keyword
    `tagset='penn'|'universal'|'stts'` (defaults to `penn`)
-   Parsing (`PatternParser`) with all `pattern` keywords, plus
    `pprint=True` (defaults to `False`)
-   Noun Phrase Extraction (`PatternParserNPExtractor`)
-   Lemmatization (`PatternParserLemmatizer`)
-   Polarity detection (`PatternAnalyzer`) - Still **EXPERIMENTAL**,
    does not yet have information on subjectivity
-   Full `pattern.text.de` API support on Python3
-   Supports Python 2 and 3
-   See [working features
    overview](http://langui.ch/nlp/python/textblob-de-dev/) for details

Installing/Upgrading
--------------------

    $ pip install -U textblob-de
    $ python -m textblob.download_corpora

Or the latest development release (apparently this does not always work
on Windows see [issues \#1744/5](https://github.com/pypa/pip/pull/1745)
for details):

    $ pip install -U git+https://github.com/markuskiller/textblob-de.git@dev
    $ python -m textblob.download_corpora

Note

`TextBlob` will be installed/upgraded automatically when running
`pip install`. The second line (`python -m textblob.download_corpora`)
downloads/updates nltk corpora and language models used in `TextBlob`.

Usage
-----

``` python
>>> from textblob_de import TextBlobDE as TextBlob
>>> text = '''Heute ist der 3. Mai 2014 und Dr. Meier feiert seinen 43. Geburtstag. 
Ich muss unbedingt daran denken, Mehl, usw. für einen Kuchen einzukaufen. Aber leider 
habe ich nur noch EUR 3.50 in meiner Brieftasche.'''
>>> blob = TextBlob(text)
>>> blob.sentences
[Sentence("Heute ist der 3. Mai 2014 und Dr. Meier feiert seinen 43. Geburtstag."),
 Sentence("Ich muss unbedingt daran denken, Mehl, usw. für einen Kuchen einzukaufen."),
 Sentence("Aber leider habe ich nur noch EUR 3.50 in meiner Brieftasche.")]
>>> blob.tokens
WordList(['Heute', 'ist', 'der', '3.', 'Mai', ...]
>>> blob.tags
[('Heute', 'RB'), ('ist', 'VB'), ('der', 'DT'), ('3.', 'LS'), ('Mai', 'NN'), 
('2014', 'CD'), ...]
# Default: Only noun_phrases that consist of two or more meaningful parts are displayed.
# Not perfect, but a start (relies heavily on parser accuracy)
>>> blob.noun_phrases
WordList(['Mai 2014', 'Dr. Meier', 'seinen 43. Geburtstag', 'Kuchen einzukaufen', 
'meiner Brieftasche'])
```

``` python
>>> blob = TextBlob("Das Auto ist sehr schön.")
>>> blob.parse()
'Das/DT/B-NP/O Auto/NN/I-NP/O ist/VB/B-VP/O sehr/RB/B-ADJP/O schön/JJ/I-ADJP/O'
>>> from textblob_de import PatternParser
>>> blob = TextBlobDE("Das ist ein schönes Auto.", parser=PatternParser(pprint=True, lemmata=True))
>>> blob.parse()
      WORD   TAG    CHUNK   ROLE   ID     PNP    LEMMA   

       Das   DT     -       -      -      -      das     
       ist   VB     VP      -      -      -      sein    
       ein   DT     NP      -      -      -      ein     
   schönes   JJ     NP ^    -      -      -      schön   
      Auto   NN     NP ^    -      -      -      auto    
         .   .      -       -      -      -      .       
>>> from textblob_de import PatternTagger
>>> blob = TextBlob(text, pos_tagger=PatternTagger(include_punc=True))
[('Das', 'DT'), ('Auto', 'NN'), ('ist', 'VB'), ('sehr', 'RB'), ('schön', 'JJ'), ('.', '.')]
```

``` python
>>> blob = TextBlob("Das Auto ist sehr schön.")
>>> blob.sentiment
Sentiment(polarity=1.0, subjectivity=0.0)
>>> blob = TextBlob("Das ist ein hässliches Auto.")     
>>> blob.sentiment
Sentiment(polarity=-1.0, subjectivity=0.0)
```

Warning

**WORK IN PROGRESS:** The German polarity lexicon contains only
uninflected forms and there are no subjectivity scores yet. As of
version 0.2.3, lemmatized word forms are submitted to the
`PatternAnalyzer`, increasing the accuracy of polarity values. New in
version 0.2.7: return type of `.sentiment` is now adapted to the main
[TextBlob](http://textblob.readthedocs.org/en/dev/) library
(`:rtype: namedtuple`).

``` python
>>> blob.words.lemmatize()
WordList(['das', 'sein', 'ein', 'hässlich', 'Auto'])
>>> from textblob_de.lemmatizers import PatternParserLemmatizer
>>> _lemmatizer = PatternParserLemmatizer()
>>> _lemmatizer.lemmatize("Das ist ein hässliches Auto.")
[('das', 'DT'), ('sein', 'VB'), ('ein', 'DT'), ('hässlich', 'JJ'), ('Auto', 'NN')]
```

Note

Make sure that you use unicode strings on Python2 if your input contains
non-ascii characters (e.g. `word = u"schön"`).

Access to `pattern` API in Python3
----------------------------------

``` python
>>> from textblob_de.packages import pattern_de as pd
>>> print(pd.attributive("neugierig", gender=pd.FEMALE, role=pd.INDIRECT, article="die"))
neugierigen
```

Note

Alternatively, the path to `textblob_de/ext` can be added to the
`PYTHONPATH`, which allows the use of `pattern.de` in almost the same
way as described in its
[Documentation](http://www.clips.ua.ac.be/pages/pattern-de). The only
difference is that you will have to prepend an underscore:
`from _pattern.de import ...`. This is a precautionary measure in case
the `pattern` library gets native Python3 support in the future.

Documentation and API Reference
-------------------------------

-   <http://textblob-de.readthedocs.org/en/latest>

Requirements
------------

-   Python &gt;= 2.6 or &gt;= 3.3

TODO
----

-   [Planned
    Extensions](http://textblob-de.readthedocs.org/en/latest/extensions.html)
-   Additional PoS tagging options, e.g. NLTK tagging (`NLTKTagger`)
-   Improve noun phrase extraction (e.g. based on `RFTagger` output)
-   Improve sentiment analysis (find suitable subjectivity scores)
-   Improve functionality of `Sentence()` and `Word()` objects
-   Adapt more tests from the main
    [TextBlob](http://textblob.readthedocs.org/en/dev/) library (esp.
    for `TextBlobDE()` in `test_blob.py`)

License
-------

MIT licensed. See the bundled
[LICENSE](https://github.com/markuskiller/textblob-de/blob/master/LICENSE)
file for more details.

Thanks
------

Coded with Wing IDE (free open source developer license)

[![Python IDE for Python - wingware.com](https://wingware.com/images/wingware-logo-180x58.png)](https://wingware.com/store/free)

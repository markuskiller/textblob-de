===========
textblob-de
===========

.. image:: https://badge.fury.io/py/textblob-de.png
    :target: http://badge.fury.io/py/textblob-de
    :alt: Latest version

.. image:: https://travis-ci.org/markuskiller/textblob-de.png?branch=dev
    :target: https://travis-ci.org/markuskiller/textblob-de
    :alt: Travis-CI

.. image:: https://pypip.in/d/textblob-de/badge.png
    :target: https://crate.io/packages/textblob-de/
    :alt: Number of PyPI downloads

.. image:: https://badge.waffle.io/markuskiller/textblob-de.png?label="In Progress"
     :target: https://waffle.io/markuskiller/textblob-de
     :alt: Issues in Ready



German language support for `TextBlob <https://textblob.readthedocs.org/>`_ by Steven Loria.

This python package is being developed as a ``TextBlob`` **Language Extension**.
See `Extension Guidelines <https://textblob.readthedocs.org/en/dev/contributing.html>`_ for details.


Features
--------

* All directly accessible ``textblob_de`` classes (e.g. ``Sentence()`` or ``Word()``) are initialized with default models for German
* Properties or methods that do not yet work for German raise a ``NotImplementedError``
* German sentence boundary detection and tokenization (``NLTKPunktTokenizer``)
* Consistent use of specified tokenizer for all tools (``NLTKPunktTokenizer`` or ``PatternTokenizer``)
* Part-of-speech tagging (``PatternTagger``) with keyword ``include_punc=True`` (defaults to ``False``)
* Parsing (``PatternParser``) with all ``pattern`` keywords, plus ``pprint=True`` (defaults to ``False``)
* Noun Phrase Extraction (``PatternParserNPExtractor``)
* Lemmatization (``PatternParserLemmatizer``)
* Polarity detection (``PatternAnalyzer``) - Still **EXPERIMENTAL**, does not yet have information on subjectivity
* **NEW:** Full ``pattern.text.de`` API support on Python3
* Supports Python 2 and 3
* See `working features overview <http://langui.ch/nlp/python/textblob-de-dev/>`_ for details


Installing/Upgrading
--------------------
::

    $ pip install -U textblob-de
    $ python -m textblob.download_corpora
    
Or the latest development release (apparently this does not always work on Windows see 
`issues #1744/5 <https://github.com/pypa/pip/pull/1745>`_ for details)::

    $ pip install -U git+https://github.com/markuskiller/textblob-de.git@dev
    $ python -m textblob.download_corpora


.. note::

   ``TextBlob`` will be installed/upgraded automatically when running 
   ``pip install``. The second line (``python -m textblob.download_corpora``) 
   downloads/updates nltk corpora and language models used in ``TextBlob``.


Usage
-----

.. code-block:: python

    >>> from textblob_de import TextBlobDE as TextBlob
    >>> text = '''Heute ist der 3. Mai 2014 und Dr. Meier feiert seinen 43. Geburtstag. 
    Ich muss unbedingt daran denken, Mehl, usw. für einen Kuchen einzukaufen. Aber leider 
    habe ich nur noch EUR 18.50 in meiner Brieftasche.'''
    >>> blob = TextBlob(text)
    >>> blob.sentences
    [Sentence("Heute ist der 3. Mai 2014 und Dr. Meier feiert seinen 43. Geburtstag."),
     Sentence("Ich muss unbedingt daran denken, Mehl, usw. für einen Kuchen einzukaufen."),
     Sentence("Aber leider habe ich nur noch EUR 18.50 in meiner Brieftasche.")]
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
    

.. code-block:: python

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


.. code-block:: python
    
    >>> blob = TextBlob("Das Auto ist sehr schön.")
    >>> blob.sentiment
    Sentiment(polarity=1.0, subjectivity=0.0)
    >>> blob = TextBlob("Das ist ein hässliches Auto.")     
    >>> blob.sentiment
    Sentiment(polarity=-1.0, subjectivity=0.0)


.. warning::

    **WORK IN PROGRESS:** The German polarity lexicon contains only uninflected
    forms and there are no subjectivity scores yet. As of version 0.2.3, lemmatized
    word forms are submitted to the ``PatternAnalyzer``, increasing the accuracy
    of polarity values. New in version 0.2.7: return type of ``.sentiment`` is now
    adapted to ``textblob`` main package (``:rtype: namedtuple``).


.. code-block:: python

    >>> blob.words.lemmatize()
    WordList(['das', 'sein', 'ein', 'hässlich', 'Auto'])
    >>> from textblob_de.lemmatizers import PatternParserLemmatizer
    >>> _lemmatizer = PatternParserLemmatizer()
    >>> _lemmatizer.lemmatize("Das ist ein hässliches Auto.")
    [('das', 'DT'), ('sein', 'VB'), ('ein', 'DT'), ('hässlich', 'JJ'), ('Auto', 'NN')]


.. note::

    Make sure that you use unicode strings on Python2 if your input contains
    non-ascii characters (e.g. ``word = u"schön"``).


Access to ``pattern`` API in Python3
------------------------------------

.. code-block:: python

    >>> from textblob_de.packages import pattern_de as pd
    >>> print(pd.attributive("neugierig", gender=pd.FEMALE, role=pd.INDIRECT, article="die"))
    neugierigen
    
.. note::

   Alternatively, the path to ``textblob_de/ext`` can be added to the ``PYTHONPATH``, which allows
   the use of ``pattern.de`` in almost the same way as described in its 
   `Documentation <http://www.clips.ua.ac.be/pages/pattern-de>`_.
   The only difference is that you will have to prepend an underscore: 
   ``from _pattern.de import ...``. This is a precautionary measure in case the ``pattern``
   library gets native Python3 support in the future.


Requirements
------------

- Python >= 2.6 or >= 3.3

TODO
----

- **TextBlob Extension:** ``textblob-rftagger`` (wrapper class for ``RFTagger``)
- **TextBlob Extension:** ``textblob-cmd`` (command-line wrapper for ``TextBlob``, basically TextBlob for files 
- **TextBlob Extension:** ``textblob-stanfordparser`` (wrapper class for ``StanfordParser`` via NLTK)
- **TextBlob Extension:** ``textblob-berkeleyparser`` (wrapper class for ``BerkeleyParser``)
- **TextBlob Extension:** ``textblob-sent-align`` (sentence alignment for parallel TextBlobs)
- **TextBlob Extension:** ``textblob-converters`` (various input and output conversions)
- Additional PoS tagging options, e.g. NLTK tagging (``NLTKTagger``)
- Improve noun phrase extraction (e.g. based on ``RFTagger`` output)
- Improve sentiment analysis (find suitable subjectivity scores)
- Improve functionality of ``Sentence()`` and ``Word()`` objects
- Adapt more tests from ``textblob`` main package (esp. for ``TextBlobDE()`` in ``test_blob.py``)


License
-------

MIT licensed. See the bundled ``LICENSE``  file for more details.


Thanks
------

Coded with Wing IDE 5.0 (free open source developer license)

.. image:: https://wingware.com/images/wingware-logo-180x58.png
    :target: https://wingware.com/store/free
    :alt: Python IDE for Python - wingware.com
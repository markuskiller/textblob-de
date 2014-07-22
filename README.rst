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


German language support for `TextBlob <https://textblob.readthedocs.org/>`_ by Steven Loria.

This python package is being developed as a ``TextBlob`` **Language Extension**.
See `Extension Guidelines <https://textblob.readthedocs.org/en/dev/contributing.html>`_ for details.


Features
--------

* ``TextBlobDE/BlobberDE/Sentence/WordList/Word``classes with initialized default models for German
* German sentence boundary detection and tokenization (``NLTKPunktTokenizer``)
* Consistent use of specified tokenizer for all tools (``NLTKPunktTokenizer`` or ``PatternTokenizer``)
* Part-of-speech tagging (``PatternTagger``) with keyword ``include_punc=True`` (defaults to ``False``)
* Parsing (``PatternParser``) with keyword ``lemmata=True`` (defaults to ``False``)
* Noun Phrase Extraction (``PatternParserNPExtractor``)
* Polarity detection (``PatternAnalyzer``) **EXPERIMENTAL** (only recognises uninflected word forms and does not have information on subjectivity)
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
    # not perfect, but a start (relies heavily on parser accuracy)
    >>> blob.noun_phrases
    WordList(['Mai 2014', 'Dr. Meier', 'seinen 43. Geburtstag', 'Kuchen einzukaufen', 
    'meiner Brieftasche'])
    

.. code-block:: python

    >>> blob = TextBlob("Das Auto ist sehr schön.")
    >>> blob.parse()
    'Das/DT/B-NP/O Auto/NN/I-NP/O ist/VB/B-VP/O sehr/RB/B-ADJP/O schön/JJ/I-ADJP/O'
    >>> from textblob_de import PatternParser
    >>> blob = TextBlob(text, parser=PatternParser(lemmata=True))
    'Das/DT/B-NP/O/das Auto/NN/I-NP/O/auto ist/VB/B-VP/O/sein sehr/RB/B-ADJP/O/sehr' \ 
    'schön/JJ/I-ADJP/O/schön ././O/O/.'
    >>> from textblob_de import PatternTagger
    >>> blob = TextBlob(text, pos_tagger=PatternTagger(include_punc=True))
    [('Das', 'DT'), ('Auto', 'NN'), ('ist', 'VB'), ('sehr', 'RB'), ('schön', 'JJ'), ('.', '.')]



.. code-block:: python
    
    >>> blob = TextBlob("Das Auto ist sehr schön.")
    >>> blob.sentiment
    (1.0, 0.0)
    >>> blob = TextBlob("Das Auto ist hässlich.")     
    >>> blob.sentiment
    (-1.0, 0.0)


.. warning::

    **WORK IN PROGRESS:** The German polarity lexicon contains only uninflected
    forms and there are no subjectivity scores yet.

.. note::

    Make sure that you use unicode strings on Python2 if your input contains
    non-ascii characters (e.g. ``word = u"schön"``).


Requirements
------------

- Python >= 2.6 or >= 3.3

TODO
----

- Additional PoS tagging options NLTK tagging (``NLTKTagger``)
- Improve sentiment analysis (find suitable subjectivity scores and look up lemmas rather than word forms)
- Improve functionality of ``Sentence()`` and ``Word()`` objects
- Adapt more tests from ``textblob`` main package (esp. for ``TextBlobDE()`` in ``test_blob.py``)

License
-------

MIT licensed. See the bundled ``LICENSE``  file for more details.

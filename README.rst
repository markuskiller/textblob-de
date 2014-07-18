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


German language support for `TextBlob <https://textblob.readthedocs.org/>`_.

This python package is being developed as a ``TextBlob`` **Language Extension**.
See `Extension Guidelines <https://textblob.readthedocs.org/en/dev/contributing.html>`_ for details.


Features
--------

* ``TextBlobDE`` class with initialized default models for German
* Improved German sentence boundary detection (``NLTKPunktTokenizer``)
* Consistent use of specified tokenizer for all tools (``NLTKPunktTokenizer`` and ``PatternTokenizer``)
* Part-of-speech tagging (``PatternTagger``)
* Parsing (``PatternParser``)
* Polarity detection (``PatternAnalyzer``) **EXPERIMENTAL!** (only recognises uninflected word forms and does not have information on subjectivity)
* Supports Python 2 and 3
* See `working features overview <http://langui.ch/nlp/python/textblob-de-dev/>`_ for details


Installing/Upgrading
--------------------
::

    $ pip install -U textblob-de
    $ python -m textblob.download_corpora
    
Or the latest development release::

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
    >>> text = "Das Auto ist sehr schön."
    >>> blob = TextBlob(text)
    >>> blob.tags
    [('Das', 'DT'), ('Auto', 'NN'), ('ist', 'VB'), ('sehr', 'RB'), ('schön', 'JJ')]
    >>> blob.parse()
    'Das/DT/B-NP/O Auto/NN/I-NP/O ist/VB/B-VP/O sehr/RB/B-ADJP/O schön/JJ/I-ADJP/O'
    >>> blob.sentiment
    (1.0, 0.0)
    >>> text = "Das Auto ist hässlich."
    >>> blob = TextBlob(text)     
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

- Additional POS Tagging Options NLTK tagging (``NLTKTagger``)
- Parsing (make keyword arguments of ``PatternParser.parse()`` accessible to make use of built-in lemmatization)
- Improve Sentiment analysis (find suitable subjectivity scores and look up lemmas rather than word forms)


License
-------

MIT licensed. See the bundled ``LICENSE``  file for more details.

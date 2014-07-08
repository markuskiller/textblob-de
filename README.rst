===========
textblob-de
===========

.. image:: https://badge.fury.io/py/textblob-de.png
    :target: http://badge.fury.io/py/textblob-de
    :alt: Latest version

.. image:: https://travis-ci.org/markuskiller/textblob-de.png?branch=master
    :target: https://travis-ci.org/markuskiller/textblob-de
    :alt: Travis-CI

German language support for `TextBlob`_.

Features
--------

* Tokenization (adapted from English PatternTokenizer)
* Part-of-speech tagging (``PatternTagger``)
* Supports Python 2 and 3

Installing/Upgrading
--------------------

If you have `pip <http://www.pip-installer.org/>`_ installed (you should), run ::

    $ pip install -U textblob
    $ pip install -U git+https://github.com/markuskiller/textblob-de.git

Usage
-----
.. code-block:: python

    >>> from textblob import TextBlob
    >>> from textblob_de import PatternTagger
    >>> text = u"Was für ein schöner Morgen!"
    >>> blob = TextBlob(text, pos_tagger=PatternTagger())
    >>> blob.tags
    [(u'Was', u'DT'), (u'für', u'DT'), (u'ein', u'DT'), (u'schöner', u'JJ'), //
    (u'Morgen', u'NN'), (u'!', u'PUNC')]


Requirements
------------

- Python >= 2.6 or >= 3.4

TODO
----

- NLTK tagging
- Parsing
- Sentiment analysis (no subjectivity lexicon in `pattern-de`_)


License
-------

MIT licensed. See the bundled `LICENSE <https://github.com/markuskiller/textblob-de/blob/master/LICENSE>`_ file for more details.

.. _TextBlob: https://textblob.readthedocs.org/
.. _pattern-de: http://www.clips.ua.ac.be/pages/pattern-de

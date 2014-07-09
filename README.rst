===========
textblob-de
===========

.. image:: https://badge.fury.io/gh/markuskiller%2Ftextblob-de.svg
    :target: http://badge.fury.io/gh/markuskiller%2Ftextblob-de
    :alt: Latest version

.. image:: https://travis-ci.org/markuskiller/textblob-de.png?branch=master
    :target: https://travis-ci.org/markuskiller/textblob-de
    :alt: Travis-CI

German language support for `TextBlob`_.

Features
--------

* Part-of-speech tagging (``PatternTagger``)
* Supports Python 2 and 3

Installing/Upgrading
--------------------

If you have `pip`_ installed (you should), run ::

    $ pip install -U textblob-de
    
Or the latest development release::

    $ pip install -U git+https://github.com/markuskiller/textblob-de.git@dev


.. note::

    `TextBlob`_ will be installed and updated automatically by running the 
    above commands.

Usage
-----
.. code-block:: python

    >>> from textblob import TextBlob
    >>> from textblob_de import PatternTagger
    >>> text = "Das ist ein schönes Auto."
    >>> blob = TextBlob(text, pos_tagger=PatternTagger())
    >>> blob.tags
    [('Das', 'DT'), ('ist', 'VB'), ('ein', 'DT'), ('schönes', 'JJ'), ('Auto', 'NN')]


.. note::

    Make sure that you use unicode strings on Python2 if your input contains
    non-ascii charachters (e.g. ``word = u"schönes"``)

Requirements
------------

- Python >= 2.6 or >= 3.3

TODO
----

- Fix handling of sentence final punctuation
- German Tokenization (adapt from English PatternTokenizer)
- NLTK tagging
- Parsing
- Sentiment analysis (no subjectivity lexicon in `pattern-de`_)


License
-------

MIT licensed. See the bundled `LICENSE`_  file for more details.

.. _pip: https://pip.pypa.io/en/latest/installing.html
.. _TextBlob: https://textblob.readthedocs.org/
.. _pattern-de: http://www.clips.ua.ac.be/pages/pattern-de
.. _LICENSE: https://github.com/markuskiller/textblob-de/blob/master/LICENSE

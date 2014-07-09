===========
textblob-de
===========

.. image:: https://badge.fury.io/py/textblob-de.png
    :target: http://badge.fury.io/py/textblob-de
    :alt: Latest version

.. image:: https://travis-ci.org/markuskiller/textblob-de.png
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

* Part-of-speech tagging (``PatternTagger``)
* Supports Python 2 and 3


Installing/Upgrading
--------------------
::

    $ pip install -U textblob-de
    
Or the latest development release::

    $ pip install -U git+https://github.com/markuskiller/textblob-de.git@dev


.. note::

   ``TextBlob`` will be installed and updated automatically by running the 
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
    non-ascii characters (e.g. ``word = u"schönes"``)


Requirements
------------

- Python >= 2.6 or >= 3.3

TODO
----

- Fix handling of sentence final punctuation
- German Tokenization (adapt English ``PatternTokenizer``)
- NLTK tagging
- Parsing
- Sentiment analysis (no subjectivity lexicon readily available in ``pattern-de``)


License
-------

MIT licensed. See the bundled ``LICENSE``  file for more details.

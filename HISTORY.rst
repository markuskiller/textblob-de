Changelog
---------

0.4.2 (02/05/2015)
++++++++++++++++++

* Removed dependency on `NLTK, <https://github.com/nltk/nltk/>`_ as it already is a `TextBlob <http://textblob.readthedocs.org/en/dev/>`_ dependency
* Temporary workaround for `NLTK Issue #824 <https://github.com/nltk/nltk/issues/824>`_ for tox/Travis-CI
* (update 13/01/2015) `NLTK Issue #824 <https://github.com/nltk/nltk/issues/824>`_ fixed, workaround removed
* Enabled ``pattern`` tagset conversion (``'penn'|'universal'|'stts'``) for ``PatternTagger``
* Added tests for tagset conversion
* Fixed test for Arabic translation example (Google translation has changed)
* Added tests for lemmatizer
* Bugfix: ``PatternAnalyzer`` no longer breaks on subsequent ocurrences of the same ``(word, tag)`` pairs on Python3 see comments to `Pull Request #11 <https://github.com/markuskiller/textblob-de/pull/11>`_
* Bugfix/performance enhancement: Sentiment dictionary in ``PatternAnalyzer`` no longer reloaded for every sentence `Pull Request #11 <https://github.com/markuskiller/textblob-de/pull/11>`_ (tanks @Arttii)

0.4.1 (03/10/2014)
++++++++++++++++++

* Docs hosted on `RTD <http://textblob-de.readthedocs.org>`_
* Removed dependency on nltk's depricated ``PunktWordTokenizer`` and replaced it with ``TreebankWordTokenizer`` see  `nltk/nltk#746 (comment) <https://github.com/nltk/nltk/pull/746#issuecomment-57625756>`_ for details

0.4.0 (17/09/2014)
++++++++++++++++++

* Fixed `Issue #7 <https://github.com/markuskiller/textblob-de/issues/7>`_ (restore ``textblob>=0.9.0`` compatibility)
* Depend on ``nltk3``. Vendorized ``nltk`` was removed in ``textblob>=0.9.0``
* Fixed ``ImportError`` on Python2 (``unicodecsv``)


0.3.1 (29/08/2014)
++++++++++++++++++

* Improved ``PatternParserNPExtractor`` (less false positives in verb filter)
* Made sure that all keyword arguments with default ``None`` are checked with ``is not None``
* Fixed shortcut to ``_pattern.de`` in vendorized library
* Added ``Makefile`` to facilitate development process
* Added docs and API reference

0.3.0 (14/08/2014)
++++++++++++++++++

* Fixed `Issue #5 <https://github.com/markuskiller/textblob-de/issues/5>`_ (text + space + period)

0.2.9 (14/08/2014)
++++++++++++++++++

* Fixed tokenization in ``PatternParser`` (if initialized manually, punctuation was not always separated from words)
* Improved handling of empty strings (Issue #3) and of strings containing single punctuation marks (Issue #4) in ``PatternTagger`` and ``PatternParser``
* Added tests for empty strings and for strings containing single punctuation marks

0.2.8 (14/08/2014)
++++++++++++++++++

* Fixed `Issue #3 <https://github.com/markuskiller/textblob-de/issues/3>`_ (empty string)
* Fixed `Issue #4 <https://github.com/markuskiller/textblob-de/issues/4>`_ (space + punctuation)

0.2.7 (13/08/2014)
++++++++++++++++++

* Fixed `Issue #1 <https://github.com/markuskiller/textblob-de/issues/1>`_ lemmatization of strings containing a forward slash (``/``)
* Enhancement `Issue #2 <https://github.com/markuskiller/textblob-de/issues/2>`_ use the same rtype as ``textblob`` for sentiment detection.
* Fixed tokenization in ``PatternParserLemmatizer``

0.2.6 (04/08/2014)
++++++++++++++++++

* Fixed ``MANIFEST.in`` for package data in ``sdist``

0.2.5 (04/08/2014)
++++++++++++++++++

* ``sdist`` is non-functional as important files are missing due to a misconfiguration in ``MANIFEST.in`` - does not affect ``wheels``
* Major internal refactoring (but no backwards-incompatible API changes) with the aim of restoring complete compatibility to original ``pattern>=2.6`` library on Python2
* Separation of ``textblob`` and ``pattern`` code
* On Python2 the vendorized version of ``pattern.text.de`` is only used if original is not installed (same as ``nltk``)
* Made ``pattern.de.pprint`` function and all parser keywords accessible to customise parser output
* Access to complete ``pattern.text.de`` API on Python2 and Python3 ``from textblob_de.packages import pattern_de as pd``
* ``tox`` passed on all major platforms (Win/Linux/OSX)

0.2.3 (26/07/2014)
++++++++++++++++++

* Lemmatizer: ``PatternParserLemmatizer()`` extracts lemmata from Parser output
* Improved polarity analysis through look-up of lemmatised word forms

0.2.2 (22/07/2014)
++++++++++++++++++

* Option: Include punctuation in ``tags``/``pos_tags`` properties (``b = TextBlobDE(text, tagger=PatternTagger(include_punc=True))``)
* Added ``BlobberDE()`` class initialized with German models
* ``TextBlobDE()``, ``Sentence()``, ``WordList()`` and ``Word()`` classes are now all initialized with German models
* Restored complete API compatibility with ``textblob.tokenizers`` module of the main `TextBlob <http://textblob.readthedocs.org/en/dev/>`_ library

0.2.1 (20/07/2014)
++++++++++++++++++

* Noun Phrase Extraction: ``PatternParserNPExtractor()`` extracts NPs from Parser output
* Refactored the way ``TextBlobDE()`` passes on arguments and keyword arguments to individual tools
* *Backwards-incompatible*: Deprecate ``parser_show_lemmata=True`` keyword in ``TextBlob()``. Use ``parser=PatternParser(lemmata=True)`` instead.

0.2.0 (18/07/2014)
++++++++++++++++++

* vastly improved tokenization (``NLTKPunktTokenizer`` and ``PatternTokenizer`` with tests)
* consistent use of specified tokenizer for all tools
* ``TextBlobDE`` with initialized default models for German
* Parsing (``PatternParser``) plus ``test_parsers.py``
* **EXPERIMENTAL** implementation of Polarity detection (``PatternAnalyzer``)
* first attempt at extracting German Polarity clues into ``de-sentiment.xml``
* tox tests passing for py26, py27, py33 and py34

0.1.3 (09/07/2014)
++++++++++++++++++

* First release on PyPI

0.1.0 - 0.1.2 (09/07/2014)
++++++++++++++++++++++++++

* First release on github
* A number of experimental releases for testing purposes
* Adapted version badges, tests & travis-ci config
* Code adapted from sample extension `textblob-fr <https://github.com/sloria/textblob-fr>`_
* Language specific linguistic resources copied from `pattern-de <https://github.com/clips/pattern/tree/master/pattern/text/de>`_

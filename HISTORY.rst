Changelog
---------

0.2.1 (unreleased)
++++++++++++++++++

* Noun Phrase Extraction: ``PatternParserNPExtractor()`` extracts NPs from Parser output

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

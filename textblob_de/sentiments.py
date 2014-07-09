# -*- coding: utf-8 -*-
"""German sentiment analysis implementations.

.. todo::

       extract/compute/compile German Subjectivity Lexicon from
       publicly available resources.
       
       Possible sources:
       
       * Wait for ``de-sentiment.xml`` to be added to `pattern-de`_
       * `German Polarity Lexicon`_
       * `IGGSA`_ (Interest Group on German Sentiment Analysis)
       * `GermanPolarityClues`_ - A Lexical Resource for German Sentiment Analysis


.. _pattern-de: http://www.clips.ua.ac.be/pages/pattern-de
.. _German Polarity Lexicon: http://bics.sentimental.li/index.php/downloads/
.. _IGGSA: https://sites.google.com/site/iggsahome/
.. _GermanPolarityClues: http://www.ulliwaltinger.de/sentiment/
"""
from __future__ import absolute_import
from textblob.base import BaseSentimentAnalyzer, CONTINUOUS
from textblob_de.de import sentiment as pattern_sentiment


class PatternAnalyzer(BaseSentimentAnalyzer):

    '''Sentiment analyzer that uses the same implementation as the
    pattern library. Returns results as a tuple of the form:

    ``(polarity, subjectivity)``
    '''

    kind = CONTINUOUS

    def analyze(self, text):
        """Return the sentiment as a tuple of the form:
        ``(polarity, subjectivity)``
        """
        #raise NotImplementedError
        return pattern_sentiment(text)

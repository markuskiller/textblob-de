# -*- coding: utf-8 -*-
"""German sentiment analysis implementations.

Code adapted from ``textblob-fr`` sample extension.

:repo: `https://github.com/sloria/textblob-fr`_
:source: textblob_fr/sentiments.py
:version: 2013-10-28 (a88e86a76a)

:modified: July 2014 <m.killer@langui.ch>

Main resource for ``de-sentiment.xml``:

* `German Polarity Lexicon <http://bics.sentimental.li/index.php/downloads>`_
* See xml comment section in ``de-sentiment.xml`` for details

.. todo::

       enhance German Polarity Lexicon, using publicly available resources.
       
       Missing values:
       
       * Subjectivity
       * (Intensity)
       
       Possible sources:
       
       * `Pattern Projext <http://www.clips.ua.ac.be/pages/pattern>`_
       
           * fr-sentiment.xml / en-sentiment.xml / nl-sentiment.xml
           
       * `IGGSA <https://sites.google.com/site/iggsahome/>`_

    :param tokenizer: (optional) A tokenizer instance. If ``None``, defaults to
        :class:`PatternTokenizer() <textblob_de.tokenizers.PatternTokenizer>`.
"""
from __future__ import absolute_import
from textblob.base import BaseSentimentAnalyzer, CONTINUOUS
from textblob_de.tokenizers import PatternTokenizer
from textblob_de.de import sentiment as pattern_sentiment


class PatternAnalyzer(BaseSentimentAnalyzer):

    '''Sentiment analyzer that uses the same implementation as the
    pattern library. Returns results as a tuple of the form:

    ``(polarity, subjectivity)``
    '''
    def __init__(self, tokenizer=None):
        self.tokenizer = tokenizer if tokenizer else PatternTokenizer()
    
    def analyze(self, text):
        """Return the sentiment as a tuple of the form:
        ``(polarity, subjectivity)``
        
        :param str text: A string.
        """
        return pattern_sentiment(text, self.tokenizer)

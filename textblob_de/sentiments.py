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
from textblob_de.lemmatizers import PatternParserLemmatizer
from textblob_de.de import sentiment as pattern_sentiment


class PatternAnalyzer(BaseSentimentAnalyzer):

    '''Sentiment analyzer that uses the same implementation as the
    pattern library. Returns results as a tuple of the form:

    ``(polarity, subjectivity)``
    '''
    def __init__(self, tokenizer=None, lemmatizer=None, lemmatize=True):
        self.tokenizer = tokenizer if tokenizer else PatternTokenizer()
        self.lemmatize = lemmatize if lemmatize else True
        if self.lemmatize:
            self.lemmatizer = lemmatizer if lemmatizer \
                else PatternParserLemmatizer(tokenizer=self.tokenizer)
        
    
    def analyze(self, text):
        """Return the sentiment as a tuple of the form:
        ``(polarity, subjectivity)``
        
        :param str text: A string.
        
        .. todo::
        
            Figure out best format to be passed to the analyzer.
            There might be a better format than a string of space separated
            lemmas (e.g. with pos tags) but the parsing/tagging
            results look rather inaccurate and a wrong pos
            might prevent the lexicon lookup of an otherwise correctly 
            lemmatized word form (or would it not?) - further checks needed.
            
        """
        if self.lemmatize:
            text = self._lemmatize(text)
        _sentiment = pattern_sentiment(text, self.tokenizer)
        return _sentiment
    
    def _lemmatize(self, raw):
        # returns a list of [(lemma1, tag1), (lemma2, tag2), ...]
        _lemmas = self.lemmatizer.lemmatize(raw)
        # pass to analyzer as a string
        _lemmas = " ".join([l for l, t  in _lemmas])
        return _lemmas
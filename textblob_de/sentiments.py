# -*- coding: utf-8 -*-
#
# Code adapted from ``textblob-fr`` sample extension.
#
# :repo: `https://github.com/sloria/textblob-fr`_
# :source: textblob_fr/sentiments.py
# :version: 2013-10-28 (a88e86a76a)
#
# :modified: 2014-08-04 <m.killer@langui.ch>
#
"""German sentiment analysis implementations.

Main resource for ``de-sentiment.xml``:

* `German Polarity Lexicon <http://bics.sentimental.li/index.php/downloads>`_
* See xml comment section in ``de-sentiment.xml`` for details

.. todo::

       enhance German Polarity Lexicon, using publicly available resources.
       
       Missing values:
       
       * Subjectivity
       * (Intensity)
       
       Possible sources:
       
       * `Pattern Project <http://www.clips.ua.ac.be/pages/pattern>`_
       
           * fr-sentiment.xml / en-sentiment.xml / nl-sentiment.xml
           
       * `IGGSA <https://sites.google.com/site/iggsahome/>`_

    :param tokenizer: (optional) A tokenizer instance. If ``None``, defaults to
        :class:`PatternTokenizer() <textblob_de.tokenizers.PatternTokenizer>`.
"""
from __future__ import absolute_import
from collections import namedtuple

import os

from textblob_de.base import BaseSentimentAnalyzer, CONTINUOUS
from textblob_de.lemmatizers import PatternParserLemmatizer
from textblob_de.packages import pattern_text
from textblob_de.tokenizers import PatternTokenizer


#################### PATTERN ANALYZER ####################################

# adapted from 'textblob_fr.fr.py'
#################### PATTERN SENTIMENT DETECTION #########################
try:
    MODULE = os.path.dirname(os.path.realpath(__file__))
except:
    MODULE = ""

_Sentiment = pattern_text.Sentiment


class Sentiment(_Sentiment):

    def load(self, path=None):
        _Sentiment.load(self, path)
        # Map "précaire" to "precaire" (without diacritics, +1% accuracy).
        if not path:
            for w, pos in list(self.items()):
                w0 = w
                if not w.endswith((u"à", u"è", u"é", u"ê", u"ï")):
                    w = w.replace(u"à", "a")
                    w = w.replace(u"é", "e")
                    w = w.replace(u"è", "e")
                    w = w.replace(u"ê", "e")
                    w = w.replace(u"ï", "i")
                if w != w0:
                    for pos, (p, s, i) in pos.items():
                        self.annotate(w, pos, p, s, i)


def pattern_sentiment(text):
    s = Sentiment(
        path=os.path.join(MODULE, "data", "de-sentiment.xml"),
        synset=None,
        negations=(
            "nicht",
            "ohne",
            "nie",
            "nein",
            "kein",
            "keiner",
            "keine",
            "nichts"),
        modifiers = ("RB", "JJ"),
        modifier = lambda w: w.endswith("lich"),
        #tokenizer = _tokenizer,
        language = "de"
    )
    return s(text)

#################### END SENTIMENT DETECTION ##################################


class PatternAnalyzer(BaseSentimentAnalyzer):

    '''Sentiment analyzer that uses the same implementation as the
    pattern library. Returns results as a tuple of the form:

    ``(polarity, subjectivity)``
    '''
    #: Enhancement Issue #2
    #: adapted from 'textblob.en.sentiments.py'
    kind = CONTINUOUS
    #: Return type declaration
    RETURN_TYPE = namedtuple('Sentiment', ['polarity', 'subjectivity'])    

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
        return self.RETURN_TYPE(*pattern_sentiment(text))

    def _lemmatize(self, raw):
        # returns a list of [(lemma1, tag1), (lemma2, tag2), ...]
        _lemmas = self.lemmatizer.lemmatize(raw)
        # pass to analyzer as a string
        _lemmas = " ".join([l for l, t in _lemmas])
        return _lemmas

#################### END PATTERN ANALYZER ################################

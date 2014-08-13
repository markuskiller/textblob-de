# -*- coding: utf-8 -*-
'''Extensions to Abstract base classes in ``textblob.base``

'''
from __future__ import absolute_import

from abc import ABCMeta, abstractmethod

from textblob.compat import with_metaclass

# provide all base classes for ``textblob_de``
from textblob.blob import BaseBlob
from textblob.base import BaseNPExtractor, BaseParser
from textblob.base import BaseSentimentAnalyzer
from textblob.base import BaseTagger, BaseTokenizer
from textblob.base import DISCRETE, CONTINUOUS


# Testing phase - if found useful, this baseclass could be merged into
# textblob.base

##### LEMMATIZER #####

class BaseLemmatizer(with_metaclass(ABCMeta)):

    '''Abstract base class from which all Lemmatizer classes inherit.
    Descendant classes must implement a ``lemmatize(text)`` method
    that returns a WordList of Word object with updated lemma properties.

    .. versionadded:: 0.2.3 (``textblob_de``)
    '''

    @abstractmethod
    def lemmatize(self, text):
        '''Return a list of (lemma, tag) tuples.'''
        return

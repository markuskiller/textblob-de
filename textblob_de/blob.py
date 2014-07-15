# -*- coding: utf-8 -*-
'''Code adapted from textblob main package.

:repo: `https://github.com/sloria/TextBlob`_
:source: textblob/blob.py
:version: 2013-10-21 (a88e86a76a)

:modified: July 2014 <m.killer@langui.ch>

'''
from __future__ import absolute_import

from textblob import TextBlob

from textblob_de.taggers import PatternTagger
from textblob_de.parsers import PatternParser
from textblob_de.sentiments import PatternAnalyzer


class TextBlobDE(TextBlob):

    '''Pass German default values to TextBlob():
    
    :param str text: A string.
    :param tokenizer: (optional) A tokenizer instance. If ``None``, defaults to
        :class:`WordTokenizer() <textblob.tokenizers.WordTokenizer>`.
    :param np_extractor: (optional) An NPExtractor instance. If ``None``,
        defaults to :class:`FastNPExtractor() <textblob.en.np_extractors.FastNPExtractor>`.
    :param pos_tagger: (optional) A Tagger instance. If ``None``, defaults to
        :class:`PatternTagger <textblob.en.taggers.PatternTagger>`.
    :param analyzer: (optional) A sentiment analyzer. If ``None``, defaults to
        :class:`PatternAnalyzer <textblob.en.sentiments.PatternAnalyzer>`.
    :param classifier: (optional) A classifier.

    '''
    analyzer = PatternAnalyzer()
    pos_tagger = PatternTagger()
    parser = PatternParser()
    classifier = None
    
    

    def __init__(self, text, 
                 tokenizer=None,
                 pos_tagger=None, 
                 np_extractor=None, 
                 analyzer=None,
                 parser=None, 
                 classifier=None, 
                 clean_html=False):
        '''Initialize TextBlob() with German default values.'''
        from textblob.utils import lowerstrip
        self.raw = self.string = text
        self.stripped = lowerstrip(self.raw, all=True)
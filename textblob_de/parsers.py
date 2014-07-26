# -*- coding: utf-8 -*-
'''Code imported from ``textblob`` main package.

:repo: `https://github.com/sloria/TextBlob`_
:source: textblob/en/parsers.py
:version: 2013-10-21 (a88e86a76a)

:modified: July 2014 <m.killer@langui.ch>

'''
from __future__ import absolute_import
from textblob.base import BaseParser
from textblob_de.de import parse as pattern_parse
from textblob_de.de import parsetree as pattern_parsetree
from textblob_de.tokenizers import PatternTokenizer


class PatternParser(BaseParser):

    '''Parser that uses the implementation in Tom de Smedt's pattern library.
    http://www.clips.ua.ac.be/pages/pattern-de#parser
    
    
    :param tokenizer: (optional) A tokenizer instance. If ``None``, defaults to
        :class:`PatternTokenizer() <textblob_de.tokenizers.PatternTokenizer>`.
    :param tokenize: (optional) Split punctuation marks from words? (Default ``True``)
    :param tags: (optional) Parse part-of-speech tags? (NN, JJ, ...) (Default ``True``)      
    :param chunks: (optional) Parse chunks? (NP, VP, PNP, ...) (Default ``True``)      
    :param relations: (optional) Parse chunk relations? (-SBJ, -OBJ, ...) (Default ``False``)      
    :param lemmata: (optional) Parse lemmata? (schönes => schön) (Default ``False``)      
    :param encoding: (optional) Input string encoding. (Default ``utf-8``)      
    :param tagset: (optional) Penn Treebank II (default) or UNIVERSAL.      
        
    '''
    def __init__(self, tokenizer=None, tokenize=True, tags=True, chunks=True,
                 relations=False, lemmata=False, encoding='utf-8', tagset=None):
        
        self.tokenizer = tokenizer if tokenizer else PatternTokenizer()
        self.tokenize = tokenize if tokenize else True
        self.tags = tags if tags else True
        self.chunks = chunks if chunks else True
        self.relations = relations if relations else False
        self.lemmata = lemmata if lemmata else False
        self.encoding = encoding if encoding else 'utf-8'
        self.tagset = tagset if tagset else None

    def parse(self, text):
        '''Parses the text.
        
        PatternParser.parse(**kwargs) can be passed to the parser instance and
        are documented in the class docstring.
        
        :param str text: A string.
        '''
        return pattern_parse(text, self.tokenizer, tokenize=self.tokenize, 
                             tags=self.tags, chunks=self.chunks,
                             relations=self.relations, lemmata=self.lemmata, 
                             encoding=self.encoding, tagset=self.tagset)
    
    def parsetree(self, text):
        """Returns a parsed ``pattern`` Text object from the given string."""
        return pattern_parsetree(text, self.tokenizer, tokenize=self.tokenize, 
                             tags=self.tags, chunks=self.chunks,
                             relations=self.relations, lemmata=self.lemmata, 
                             encoding=self.encoding, tagset=self.tagset)
        

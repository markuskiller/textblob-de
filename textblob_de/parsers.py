# -*- coding: utf-8 -*-
#
# Code imported from ``textblob`` main package.
#
# :repo: `https://github.com/sloria/TextBlob`_
# :source: textblob/en/parsers.py
# :version: 2013-10-21 (a88e86a76a)
#
# :modified: 2014-08-04 <m.killer@langui.ch>
#
'''Default parsers for German.

>>> from textblob_de.parsers import PatternParser

or

>>> from textblob_de import PatternParser

'''
from __future__ import absolute_import
import string

from textblob.base import BaseParser

from textblob_de.packages import pattern_de
from textblob_de.tokenizers import PatternTokenizer

pattern_pprint = pattern_de.pprint
pattern_parse = pattern_de.parse
pattern_parsetree = pattern_de.parsetree

PUNCTUATION = string.punctuation

class PatternParser(BaseParser):

    '''Parser that uses the implementation in Tom de Smedt's pattern library.
    http://www.clips.ua.ac.be/pages/pattern-de#parser


    :param tokenizer: (optional) A tokenizer instance. If ``None``, defaults to
        :class:`PatternTokenizer() <textblob_de.tokenizers.PatternTokenizer>`.
    :param tokenize: (optional) Split punctuation marks from words? (Default ``True``)
    :param pprint: (optional) Use ``pattern``'s ``pprint`` function to display parse trees (Default ``False``)
    :param tags: (optional) Parse part-of-speech tags? (NN, JJ, ...) (Default ``True``)
    :param chunks: (optional) Parse chunks? (NP, VP, PNP, ...) (Default ``True``)
    :param relations: (optional) Parse chunk relations? (-SBJ, -OBJ, ...) (Default ``False``)
    :param lemmata: (optional) Parse lemmata? (schönes => schön) (Default ``False``)
    :param encoding: (optional) Input string encoding. (Default ``utf-8``)
    :param tagset: (optional) Penn Treebank II (default) or ('penn'|'universal'|'stts').

    '''

    def __init__(self, tokenizer=None, tokenize=True, pprint=False, tags=True, chunks=True,
                 relations=False, lemmata=False, encoding='utf-8', tagset=None):

        self.tokenizer = tokenizer if tokenizer else PatternTokenizer()
        self.pprint = pprint if pprint else False
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
        #: Do not process empty strings (Issue #3)
        if text.strip() == "":
            return ""
        #: Do not process strings consisting of a single punctuation mark (Issue #4)
        elif text.strip() in PUNCTUATION:
            _sym = text.strip()
            if _sym in tuple('.?!'):
                _tag = "."
            else:
                _tag = _sym
            if self.lemmata:
                return "{0}/{1}/O/O/{0}".format(_sym, _tag)
            else:
                return "{0}/{1}/O/O".format(_sym, _tag)
        if self.tokenize:
            _tokenized = " ".join(self.tokenizer.tokenize(text))
        
        _parsed = pattern_parse(_tokenized,
                                # text is tokenized before it is passed on to
                                # pattern.de.parse
                                tokenize=False,
                                tags=self.tags, chunks=self.chunks,
                                relations=self.relations, lemmata=self.lemmata,
                                encoding=self.encoding, tagset=self.tagset)
        if self.pprint:
            _parsed = pattern_pprint(_parsed)

        return _parsed

    def parsetree(self, text):
        """Returns a parsed ``pattern`` Text object from the given string."""

        if self.tokenize:
            _tokenized = " ".join(self.tokenizer.tokenize(text))

        _parsed = pattern_parsetree(text,
                                    # text is tokenized before it is passed on
                                    # to pattern.de.parsetree
                                    tokenize=False,
                                    tags=self.tags, chunks=self.chunks,
                                    relations=self.relations, lemmata=self.lemmata,
                                    encoding=self.encoding, tagset=self.tagset)

        if self.pprint:
            _parsed = pattern_pprint(_parsed)

        return _parsed

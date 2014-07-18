# -*- coding: utf-8 -*-
'''Various tokenizer implementations.

Code adapted from ``textblob`` main package.

:repo: `https://github.com/sloria/TextBlob`_
:source: textblob/tokenizers.py
:version: 2013-12-27 (fbdcaf2709)

:modified: July 2014 <m.killer@langui.ch>

'''
from __future__ import absolute_import

import re

from itertools import chain

from textblob.packages import nltk
from textblob.utils import strip_punc
from textblob.base import BaseTokenizer
from textblob.decorators import requires_nltk_corpus

from textblob_de.compat import basestring
from textblob_de._text import find_tokens as find_sentences
from textblob_de._text import replacements, ABBREVIATIONS_DE, PUNCTUATION


def get_arg_tokenizer():
    # getattr(object, "attr_name", default value)
    tokenizer = getattr(get_arg_tokenizer, "tokenizer", NLTKPunktTokenizer())
    return tokenizer


class NLTKPunktTokenizer(BaseTokenizer):

    """Tokenizer included in ``nltk.tokenize.punkt`` package

    This is the default tokenizer in ``textblob-de``

    PROs:
    ^^^^^
    * trained model available for German
    * deals with many abbreviations and common German tokenization problems oob

    CONs
    ^^^^

    * not very flexible (model has to be re-trained on your own corpus)

    """

    def __init__(self):
        self.tokens = []
        self.sent_tok = nltk.tokenize.load('tokenizers/punkt/german.pickle')
        self.word_tok = nltk.tokenize.punkt.PunktWordTokenizer()

    def tokenize(self, text, include_punc=True, nested=False):
        '''Return a list of word tokens.

        :param text: string of text.
        :param include_punc: (optional) whether to include punctuation as separate tokens. Default to True.
        :param nested: (optional) whether to return tokens as nested lists of sentences. Default to False.
        '''
        self.tokens = [
            w for w in (
                self.word_tokenize(
                    s,
                    include_punc) for s in self.sent_tokenize(text))]
        if nested:
            return self.tokens
        else:
            return list(chain.from_iterable(self.tokens))

    @requires_nltk_corpus
    def sent_tokenize(self, text, **kwargs):
        '''NLTK's sentence tokenizer (currently PunktSentenceTokenizer).
        Uses an unsupervised algorithm to build a model for abbreviation words,
        collocations, and words that start sentences, then uses that to find
        sentence boundaries.
        '''
        sentences = self.sent_tok.tokenize(text, realign_boundaries=True)
        return sentences

    def word_tokenize(self, text, include_punc=True):
        '''NLTK's PunktWordTokenizer uses a regular expression to divide
        a text into tokens, leaving all periods attached to words,
        but separating off other punctuation.
        '''
        _tokens = self.word_tok.tokenize(text)
        if include_punc:
            last_word = _tokens[-1]
            if last_word.endswith('.'):
                _tokens = _tokens[:-1] + [last_word[:-1], '.']
            return _tokens
        else:
            # Return each word token
            # Strips punctuation unless the word comes from a contraction
            # e.g. "gibt's" => ["gibt", "'s"] in "Heute gibt's viel zu tun!"
            # e.g. "hat's" => ["hat", "'s"]
            # e.g. "home." => ['home']
            words = [word if word.startswith("'") else strip_punc(word, all=False)
                     for word in _tokens if strip_punc(word, all=False)]
            return list(words)


class PatternTokenizer(BaseTokenizer):

    """Tokenizer included in ``pattern.de`` package

    PROs:
    ^^^^^
    * handling of emoticons
    * flexible implementations of abbreviations
    * can be adapted very easily

    CONs
    ^^^^

    * ordinal numbers cause sentence breaks
    * indices of Sentence() objects cannot be computed

    """

    def __init__(self):
        self.tokens = []

    def tokenize(self, text, include_punc=True, nested=False):
        '''Return a list of word tokens.

        :param text: string of text.
        :param include_punc: (optional) whether to include punctuation as separate tokens. Default to True.
        '''
        self.tokens = [
            w for w in (
                self.word_tokenize(
                    s,
                    include_punc) for s in self.sent_tokenize(text))]
        if nested:
            return self.tokens
        else:
            return list(chain.from_iterable(self.tokens))

    def sent_tokenize(self, text, **kwargs):
        """Returns a list of sentences. Each sentence is a space-separated string of tokens (words).
        Handles common cases of abbreviations (e.g., etc., ...).
        Punctuation marks are split from other words. Periods (or ?!) mark the end of a sentence.
        Headings without an ending period are inferred by line breaks.
        """

        sentences = find_sentences(text,
                                   punctuation=kwargs.get(
                                       "punctuation",
                                       PUNCTUATION),
                                   abbreviations=kwargs.get(
                                       "abbreviations",
                                       ABBREVIATIONS_DE),
                                   replace=kwargs.get("replace", replacements),
                                   linebreak=r"\n{2,}")
        return sentences

    def word_tokenize(self, sentences, include_punc=True):

        _tokens = sentences.split(" ")

        if include_punc:
            return _tokens
        else:
            # Return each word token
            # Strips punctuation unless the word comes from a contraction
            # e.g. "gibt's" => ["gibt", "'s"] in "Heute gibt's viel zu tun!"
            # e.g. "hat's" => ["hat", "'s"]
            # e.g. "home." => ['home']
            words = [word if word.startswith("'") else strip_punc(word, all=False)
                     for word in _tokens if strip_punc(word, all=False)]
            return list(words)

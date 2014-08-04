# -*- coding: utf-8 -*-
#
# Code adapted from ``textblob`` main package.
#
# :repo: `https://github.com/sloria/TextBlob`_
# :source: textblob/tokenizers.py
# :version: 2013-12-27 (fbdcaf2709)
#
# :modified: 2014-08-04 <m.killer@langui.ch>
#
'''Various tokenizer implementations.
'''
from __future__ import absolute_import

import re
import string

from itertools import chain

from textblob.packages import nltk
from textblob.utils import strip_punc
from textblob.base import BaseTokenizer
from textblob.decorators import requires_nltk_corpus

from textblob_de.compat import basestring
from textblob_de.packages import pattern_de
from textblob_de.packages import pattern_text

find_sentences = pattern_text.find_tokens
replacements = pattern_text.replacements
PUNCTUATION = string.punctuation
ABBREVIATIONS_DE = pattern_de.ABBREVIATIONS


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
        sentences = self.sent_tok.tokenize(text,
                                           realign_boundaries=kwargs.get("realign_boundaries", True))
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
            last_word = _tokens[-1]
            if len(last_word) > 1 and last_word.endswith('.'):
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


class WordTokenizer(BaseTokenizer):

    '''Generic word tokenization class, using tokenizer specified in TextBlobDE() instance.

    You can also submit the tokenizer as keyword argument:
    ``WordTokenizer(tokenizer=NLTKPunktTokenizer())``

    Enables WordTokenizer().itokenize generator that would be lost otherwise.

    Default: NLTKPunktTokenizer().word_tokenize(text, include_punc=True)

    Aim: Not to break core API of ``textblob`` main package.

    :param tokenizer: (optional) A tokenizer instance. If ``None``, defaults to
        :class:`NLTKPunktTokenizer() <textblob_de.tokenizers.NLTKPunktTokenizer>`.
    '''

    def __init__(self, tokenizer=None, *args, **kwargs):
        # make sure that tokenizer is not referring to this class
        self.tokenizer = tokenizer if tokenizer and \
            not isinstance(tokenizer, WordTokenizer) else NLTKPunktTokenizer()

    def tokenize(self, text, include_punc=True, **kwargs):
        '''Return a list of word tokens.

        :param text: string of text.
        :param include_punc: (optional) whether to include punctuation as separate tokens. Default to True.
        '''
        return self.tokenizer.word_tokenize(text, include_punc, **kwargs)

    def word_tokenize(self, text, include_punc=True):
        '''Compatibility method to tokenizers included in ``textblob-de``'''
        return self.tokenize(text, include_punc)


class SentenceTokenizer(BaseTokenizer):

    '''Generic sentence tokenization class, using tokenizer specified in TextBlobDE() instance.

    Enables SentenceTokenizer().itokenize generator that would be lost otherwise.

    Aim: Not to break core API of ``textblob`` main package.

    :param tokenizer: (optional) A tokenizer instance. If ``None``, defaults to
        :class:`NLTKPunktTokenizer() <textblob_de.tokenizers.NLTKPunktTokenizer>`.
    '''

    def __init__(self, tokenizer=None, *args, **kwargs):
        # make sure that tokenizer is not referring to this class
        self.tokenizer = tokenizer if tokenizer and \
            not isinstance(tokenizer, SentenceTokenizer) else NLTKPunktTokenizer()

    def tokenize(self, text, **kwargs):
        '''Return a list of word tokens.

        :param text: string of text.
        :param include_punc: (optional) whether to include punctuation as separate tokens. Default to True.
        '''
        return self.tokenizer.sent_tokenize(text, **kwargs)

    def sent_tokenize(self, text, **kwargs):
        '''Compatibility method to tokenizers included in ``textblob-de``'''
        return self.tokenize(text, **kwargs)


def sent_tokenize(text, tokenizer=None):
    """Convenience function for tokenizing sentences (not iterable).

    If tokenizer is not specified, the default tokenizer NLTKPunktTokenizer()
    is used (same behaviour as in ``textblob`` main package).

    This function returns the sentences as a generator object
    """
    _tokenizer = tokenizer if tokenizer else NLTKPunktTokenizer()
    return SentenceTokenizer(tokenizer=_tokenizer).itokenize(text)


def word_tokenize(text, tokenizer=None, include_punc=True, *args, **kwargs):
    """Convenience function for tokenizing text into words.

    NOTE: NLTK's word tokenizer expects sentences as input, so the text will be
    tokenized to sentences before being tokenized to words.

    This function returns an itertools chain object (generator).
    """
    _tokenizer = tokenizer if tokenizer else NLTKPunktTokenizer()
    words = chain.from_iterable(
        WordTokenizer(tokenizer=_tokenizer).itokenize(sentence, include_punc,
                                                      *args, **kwargs)
        for sentence in sent_tokenize(text, tokenizer=_tokenizer))
    return words

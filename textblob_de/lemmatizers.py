# -*- coding: utf-8 -*-
'''Various lemmatizer implementations.

 :class:`PatternParserLemmatizer() <textblob_de.lemmatizers.PatternParserLemmatizer>`.

'''
from __future__ import absolute_import

import os
import re
import string

from itertools import chain
from collections import defaultdict

from textblob_de.base import BaseLemmatizer
from textblob_de.packages import pattern_de
from textblob_de.tokenizers import PatternTokenizer

pattern_parse = pattern_de.parse

try:
    MODULE = os.path.dirname(os.path.realpath(__file__))
except:
    MODULE = ""


class PatternParserLemmatizer(BaseLemmatizer):

    """Extract lemmas from PatternParser() output.

    Very naïve and resource hungry approach:

    * get parser output
    * return a list of (lemma, pos_tag) tuples

    :param tokenizer: (optional) A tokenizer instance. If ``None``, defaults to
        :class:`PatternTokenizer() <textblob_de.tokenizers.PatternTokenizer>`.

    .. versionadded:: 0.3.0 (``textblob_de``)
    """

    def __init__(self, tokenizer=None):
        self.tokenizer = tokenizer if tokenizer else PatternTokenizer()

    def lemmatize(self, text):
        '''Return a list of (lemma, tag) tuples.

        :param str text: A string.
        '''
        #: Do not process empty strings (Issue #3)
        if text.strip() == "":
            return []
        parsed_sentences = self._parse_text(text)
        _lemmalist = []
        for s in parsed_sentences:
            tokens = s.split()
            for i, t in enumerate(tokens):
                #: Filter empty tokens from the parser output (Issue #5)
                #: This only happens if parser input is improperly tokenized
                #: e.g. if there are empty strings in the list of tokens ['A', '', '.']
                if t.startswith('/'):
                    continue
                w, tag, phrase, role, lemma = t.split('/')
                # The lexicon uses Swiss spelling: "ss" instead of "ß".
                lemma = lemma.replace(u"ß", "ss")
                # Reverse previous replacement
                lemma = lemma.strip().replace("forwardslash", "/")
                if w[0].isupper() and i > 0:
                    lemma = lemma.title()
                elif tag.startswith("N") and i == 0:
                    lemma = lemma.title()
                # Todo: Check if it makes sense to treat '/' as punctuation
                # (especially for sentiment analysis it might be interesting 
                # to treat it as OR ('oder')).
                if w in string.punctuation or lemma == '/':
                    continue
                else:
                    lemma = lemma

                _lemmalist.append((lemma, tag))
        return _lemmalist

    def _parse_text(self, text):
        """Parse text (string) and return list of parsed sentences (strings).

        Each sentence consists of space separated token elements and the
        token format returned by the PatternParser is WORD/TAG/PHRASE/ROLE/LEMMA
        (separated by a forward slash '/')

        :param str text: A string.
        """
        # Fix for issue #1
        text = text.replace("/", " FORWARDSLASH ")
        _tokenized = " ".join(self.tokenizer.tokenize(text))
        parsed_text = pattern_parse(_tokenized, tokenize=False, lemmata=True)
        return parsed_text.split('\n')

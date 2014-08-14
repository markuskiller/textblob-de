# -*- coding: utf-8 -*-
#
# Code adapted from ``textblob-fr`` sample extension.
#
# :repo: `https://github.com/sloria/textblob-fr`_
# :source: textblob_fr/taggers.py
# :version: 2013-10-28 (5c6329d209)
#
# :modified: 2014-08-04 <m.killer@langui.ch>
#
'''Default taggers for German.

>>> from textblob_de.taggers import PatternTagger

or

>>> from textblob_de import PatternTagger
'''

from __future__ import absolute_import
import string

from textblob.base import BaseTagger
from textblob.utils import PUNCTUATION_REGEX

from textblob_de.packages import pattern_de

from textblob_de.compat import unicode
from textblob_de.tokenizers import PatternTokenizer

pattern_tag = pattern_de.tag
PUNCTUATION = string.punctuation

class PatternTagger(BaseTagger):

    '''Tagger that uses the implementation in
    Tom de Smedt's pattern library
    (http://www.clips.ua.ac.be/pattern).

    :param tokenizer: (optional) A tokenizer instance. If ``None``, defaults to
        :class:`PatternTokenizer() <textblob_de.tokenizers.PatternTokenizer>`.
    :param include_punc: (optional) whether to include punctuation as separate tokens. Default to ``False``.
    '''

    def __init__(self, tokenizer=None, include_punc=False):
        self.tokenizer = tokenizer if tokenizer else PatternTokenizer()
        self.include_punc = include_punc if include_punc else False

    def tag(self, sentence, tokenize=True):
        '''Tag a string `sentence`.

        :param str or list sentence: A string or a list of sentence strings.
        :param tokenize: (optional) If ``False`` string has to be tokenized before (space separated string).
        '''
        #: Do not process empty strings (Issue #3)
        if sentence.strip() == "":
            return []
        #: Do not process strings consisting of a single punctuation mark (Issue #4)
        elif sentence.strip() in PUNCTUATION:         
            if self.include_punc:
                _sym = sentence.strip()
                if _sym in tuple('.?!'):
                    _tag = "."
                else:
                    _tag = _sym
                return [(_sym, _tag)]
            else:
                return []
        if tokenize:
            _tokenized = " ".join(self.tokenizer.tokenize(sentence))
            sentence = _tokenized
        # Sentence is tokenized before it is passed on to pattern.de.tag
        # (i.e. it is either submitted tokenized or if )
        _tagged = pattern_tag(sentence, tokenize=False)
        if self.include_punc:
            return _tagged
        else:
            _tagged = [
                (word, t) for word, t in _tagged if not PUNCTUATION_REGEX.match(
                    unicode(t))]
            return _tagged

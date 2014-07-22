# -*- coding: utf-8 -*-
'''Code adapted from ``textblob-fr`` sample extension.

:repo: `https://github.com/sloria/textblob-fr`_
:source: textblob_fr/taggers.py
:version: 2013-10-28 (5c6329d209)

:modified: July 2014 <m.killer@langui.ch>
'''

from __future__ import absolute_import

from textblob.base import BaseTagger
from textblob.utils import PUNCTUATION_REGEX

from textblob_de.de import tag as pattern_tag

from textblob_de.compat import unicode
from textblob_de.tokenizers import PatternTokenizer


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
        :param tokenizer: (optional) If ``True``
        '''       
        _tagged = pattern_tag(sentence, self.tokenizer, tokenize)
        if self.include_punc:
            return _tagged
        else:
            _tagged = [(word, t) for word, t in _tagged if not PUNCTUATION_REGEX.match(unicode(t))]
            return _tagged

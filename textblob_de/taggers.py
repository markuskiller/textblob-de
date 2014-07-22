# -*- coding: utf-8 -*-
'''Code adapted from ``textblob-fr`` sample extension.

:repo: `https://github.com/sloria/textblob-fr`_
:source: textblob_fr/taggers.py
:version: 2013-10-28 (5c6329d209)

:modified: July 2014 <m.killer@langui.ch>
'''

from __future__ import absolute_import

from textblob.base import BaseTagger
from textblob_de.de import tag as pattern_tag

from textblob_de.tokenizers import PatternTokenizer


class PatternTagger(BaseTagger):

    '''Tagger that uses the implementation in
    Tom de Smedt's pattern library
    (http://www.clips.ua.ac.be/pattern).
    
    :param tokenizer: (optional) A tokenizer instance. If ``None``, defaults to
        :class:`PatternTokenizer() <textblob_de.tokenizers.PatternTokenizer>`.
    '''
    def __init__(self, tokenizer=None):
        self.tokenizer = tokenizer if tokenizer else PatternTokenizer()

    def tag(self, sentence, tokenize=True):
        '''Tag a string `sentence`.
        
        :param str or list sentence: A string or a list of sentence strings.
        :param tokenizer: (optional) If ``True``
        '''
        # for future implementations (needs to be changed in BaseBlob and BaseTagger)
        # def tag(self, sentence, tokenizer, tokenize=True)
        return pattern_tag(sentence, self.tokenizer, tokenize)

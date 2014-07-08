# -*- coding: utf-8 -*-
from __future__ import absolute_import

from textblob.base import BaseTagger
from textblob_de.de import tag as pattern_tag


class PatternTagger(BaseTagger):

    '''Tagger that uses the implementation in
    Tom de Smedt's pattern library
    (http://www.clips.ua.ac.be/pattern).
    '''

    def tag(self, sentence, tokenize=True):
        '''Tag a string `sentence`.'''
        return pattern_tag(sentence, tokenize)

# -*- coding: utf-8 -*-
from __future__ import absolute_import
from textblob.base import BaseParser
from textblob_de.de import parse as pattern_parse


class PatternParser(BaseParser):

    '''Parser that uses the implementation in Tom de Smedt's pattern library.
    http://www.clips.ua.ac.be/pages/pattern-de#parser
    '''

    def parse(self, text):
        '''Parses the text.'''
        return pattern_parse(text)

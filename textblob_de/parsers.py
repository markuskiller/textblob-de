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
from textblob_de.tokenizers import get_arg_tokenizer


def get_kwarg_lemmata():
    # getattr(object, "attr_name", default value)
    lemmata = getattr(get_kwarg_lemmata, "lemmata", False)
    return lemmata


class PatternParser(BaseParser):

    '''Parser that uses the implementation in Tom de Smedt's pattern library.
    http://www.clips.ua.ac.be/pages/pattern-de#parser
    '''

    def parse(self, text):
       # for future implementations (needs to be changed in BaseBlob and BaseParser)
       # def parse(self, text, tokenizer, lemmata=True):
        '''Parses the text.'''
        return pattern_parse(
            text, get_arg_tokenizer(), lemmata=get_kwarg_lemmata())

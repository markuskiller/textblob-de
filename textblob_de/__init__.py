# -*- coding: utf-8 -*-
from __future__ import absolute_import
from textblob_de.blob import TextBlobDE
from textblob_de.tokenizers import NLTKPunktTokenizer, PatternTokenizer
from textblob_de.taggers import PatternTagger
from textblob_de.parsers import PatternParser
from textblob_de.np_extractors import PatternParserNPExtractor
from textblob_de.sentiments import PatternAnalyzer


__version__ = '0.2.1'
__author__ = 'Markus Killer'
__license__ = "MIT"

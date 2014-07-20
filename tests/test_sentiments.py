#!/usr/bin/env
# -*- coding: utf-8 -*-
'''Code imported from ``textblob-fr`` sample extension.

:repo: `https://github.com/sloria/textblob-fr`_
:source: tests/test_sentiments.py
:version: 2013-09-18 (1a8438b5ea)

:modified: July 2014 <m.killer@langui.ch>

'''
from __future__ import unicode_literals
import unittest
from nose.tools import *  # PEP8 asserts

from textblob_de import TextBlobDE as TextBlob
from textblob_de import PatternAnalyzer as DeAnalyzer
from textblob_de import NLTKPunktTokenizer, PatternTokenizer


class TestPatternAnalyzer(unittest.TestCase):

    def setUp(self):
        self.neg1 = "Das Auto ist schrecklich."
        self.pos1 = "Das Auto ist schön."
        self.pos2 = "Die Katze ist nicht böse."
        self.neg2 = "Dieser Hund ist nicht nett."


    def test_analyze_nltk_tok(self):
        _analyzer = DeAnalyzer(tokenizer=NLTKPunktTokenizer())
        pos_sentiment = _analyzer.analyze(self.pos1)
        assert_true(pos_sentiment[0] > 0.0)
        neg_sentiment = _analyzer.analyze(self.neg1)
        assert_true(neg_sentiment[0] < 0.0)

    def test_blob_analyze_nltk_tok(self):
        _analyzer = DeAnalyzer(tokenizer=NLTKPunktTokenizer())
        pos_blob = TextBlob(self.pos2, analyzer=_analyzer)
        assert_true(pos_blob.sentiment[0] > 0.0)
        neg_blob = TextBlob(self.neg2, analyzer=_analyzer)
        assert_true(neg_blob.sentiment[0] < 0.0)
        
    def test_analyze_pattern_tok(self):
        _analyzer = DeAnalyzer(tokenizer=PatternTokenizer())
        pos_sentiment = _analyzer.analyze(self.pos1)
        assert_true(pos_sentiment[0] > 0.0)
        neg_sentiment = _analyzer.analyze(self.neg1)
        assert_true(neg_sentiment[0] < 0.0)

    def test_blob_analyze_pattern_tok(self):
        _analyzer = DeAnalyzer(tokenizer=PatternTokenizer())
        pos_blob = TextBlob(self.pos2, analyzer=_analyzer)
        assert_true(pos_blob.sentiment[0] > 0.0)
        neg_blob = TextBlob(self.neg2, analyzer=_analyzer)
        assert_true(neg_blob.sentiment[0] < 0.0)


if __name__ == '__main__':
    unittest.main()

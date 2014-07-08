#!/usr/bin/env
# -*- coding: utf-8 -*-
import unittest
from nose.tools import *  # PEP8 asserts

from text.blob import TextBlob
from textblob_de import PatternAnalyzer as DeAnalyzer

class TestPatternAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = DeAnalyzer()
        self.neg = u"Das ist ein schreckliches Auto."
        self.pos = u"Was für ein schöner Morgen!"

    def test_analyze(self):
        pos_sentiment = self.analyzer.analyze(self.pos)
        assert_true(pos_sentiment[0] > 0.0)
        neg_sentiment = self.analyzer.analyze(self.neg)
        assert_true(neg_sentiment[0] < 0.0)

    def test_blob_analyze(self):
        pos_blob = TextBlob(self.pos, analyzer=self.analyzer)
        assert_true(pos_blob.sentiment[0] > 0.0)
        neg_blob = TextBlob(self.neg, analyzer=self.analyzer)
        assert_true(neg_blob.sentiment[0] < 0.0)


if __name__ == '__main__':
    unittest.main()
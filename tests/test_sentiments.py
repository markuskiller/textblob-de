#!/usr/bin/env
# -*- coding: utf-8 -*-
import unittest
from nose.tools import *  # PEP8 asserts

from text.blob import TextBlob
from textblob_de import PatternAnalyzer as DeAnalyzer

class TestPatternAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = DeAnalyzer()
        self.neg1 = u"Das ist ein schreckliches Auto."
        self.pos1 = u"Das ist ein schönes Auto."
        self.pos2 = u"Das ist eine schöne Katze."
        self.neg2 = u"Diese Anlage ist nicht schön."

    def test_analyze(self):
        pos_sentiment = self.analyzer.analyze(self.pos1)
        assert_true(pos_sentiment[0] > 0.0)
        neg_sentiment = self.analyzer.analyze(self.neg1)
        assert_true(neg_sentiment[0] < 0.0)

    def test_blob_analyze(self):
        pos_blob = TextBlob(self.pos2, analyzer=self.analyzer)
        assert_true(pos_blob.sentiment[0] > 0.0)
        neg_blob = TextBlob(self.neg2, analyzer=self.analyzer)
        assert_true(neg_blob.sentiment[0] < 0.0)


if __name__ == '__main__':
    unittest.main()
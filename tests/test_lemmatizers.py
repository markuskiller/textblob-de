# -*- coding: utf-8 -*-
"""Test cases for np extractors."""
from __future__ import unicode_literals
import unittest
from nose.tools import *  # PEP8 asserts

from textblob_de import PatternParserLemmatizer, PatternTokenizer, NLTKPunktTokenizer


class TestPatternParserLemmatizer(unittest.TestCase):

    def setUp(self):
        self.text = "Peter hat ein schönes Auto."
        self.expected_lemmata = [
            ('Peter', 'NNP'), ('haben', 'VB'), ('ein', 'DT'), ('schön', 'JJ'), ('Auto', 'NN')]

    def test_lemmatize_nltk_tok(self):
        _lemmatizer = PatternParserLemmatizer(tokenizer=NLTKPunktTokenizer())
        lemmata = _lemmatizer.lemmatize(self.text)
        assert_equal(lemmata, self.expected_lemmata)

    def test_lemmatize_pattern_tok(self):
        _lemmatizer = PatternParserLemmatizer(tokenizer=PatternTokenizer())
        lemmata = _lemmatizer.lemmatize(self.text)
        assert_equal(lemmata, self.expected_lemmata)


if __name__ == '__main__':
    unittest.main()

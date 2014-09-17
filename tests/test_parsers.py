# -*- coding: utf-8 -*-
# Code adapted from the main `TextBlob`_ library.
#
# :repo: `https://github.com/sloria/TextBlob`_
# :source: tests/test_parsers.py
# :version: 2013-10-21 (a88e86a76a)
#
# :modified: 2014-08-29 <m.killer@langui.ch>
#
"""Test cases for parsers."""
from __future__ import unicode_literals

import unittest
from nose.tools import *  # PEP8 asserts


from textblob_de import NLTKPunktTokenizer
from textblob_de import PatternParser
from textblob_de import PatternTokenizer

from textblob_de.packages import pattern_de

pattern_parse = pattern_de.parse


class TestPatternParser(unittest.TestCase):

    def setUp(self):
        self.text = "Das Auto ist sehr schön."

        self.expected = "Das/DT/B-NP/O Auto/NN/I-NP/O ist/VB/B-VP/O " \
                        "sehr/RB/B-ADJP/O schön/JJ/I-ADJP/O ././O/O"

        self.expected_with_lemmata = \
            'Das/DT/B-NP/O/das Auto/NN/I-NP/O/auto ' \
            'ist/VB/B-VP/O/sein sehr/RB/B-ADJP/O/sehr ' \
            'schön/JJ/I-ADJP/O/schön ././O/O/.'

    def test_parse(self):
        parser = parser = PatternParser()
        assert_equal(parser.parse(self.text),
                     pattern_parse(self.text))

    def test_parse_nltk_tok_result_string(self):
        parser = PatternParser(tokenizer=NLTKPunktTokenizer(), lemmata=False)
        assert_equal(parser.parse(self.text), self.expected)

    def test_parse_nltk_tok_show_lemmata(self):
        parser = PatternParser(tokenizer=NLTKPunktTokenizer(), lemmata=True)
        assert_equal(parser.parse(self.text), self.expected_with_lemmata)

    def test_parse_pattern_tok_result_string(self):
        parser = PatternParser(tokenizer=PatternTokenizer(), lemmata=False)
        assert_equal(parser.parse(self.text), self.expected)

    def test_parse_pattern_tok_show_lemmata(self):
        parser = PatternParser(tokenizer=PatternTokenizer(), lemmata=True)
        assert_equal(parser.parse(self.text), self.expected_with_lemmata)


if __name__ == '__main__':
    unittest.main()

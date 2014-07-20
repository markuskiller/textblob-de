# -*- coding: utf-8 -*-
'''Code imported from ``textblob`` main package.

:repo: `https://github.com/sloria/TextBlob`_
:source: tests/test_parsers.py
:version: 2013-10-21 (a88e86a76a)

:modified: July 2014 <m.killer@langui.ch>

'''
import unittest
from nose.tools import *  # PEP8 asserts

from textblob_de import PatternParser, PatternTokenizer, NLTKPunktTokenizer
from textblob_de.de import parse as pattern_parse


class TestPatternParser(unittest.TestCase):

    def setUp(self):
        self.text = u"Das Auto ist sehr schön."

        self.expected = u"Das/DT/B-NP/O Auto/NN/I-NP/O ist/VB/B-VP/O " \
                        u"sehr/RB/B-ADJP/O schön/JJ/I-ADJP/O ././O/O"

        self.expected_with_lemmata = \
            u'Das/DT/B-NP/O/das Auto/NN/I-NP/O/auto ' \
            u'ist/VB/B-VP/O/sein sehr/RB/B-ADJP/O/sehr ' \
            u'schön/JJ/I-ADJP/O/schön ././O/O/.'


    def test_parse(self):
        parser = parser = PatternParser()
        assert_equal(parser.parse(self.text), 
                     pattern_parse(self.text, PatternTokenizer()))

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

# -*- coding: utf-8 -*-
'''Code imported from ``textblob`` main package.

:repo: `https://github.com/sloria/TextBlob`_
:source: tests/test_parsers.py
:version: 2013-10-21 (a88e86a76a)

:modified: July 2014 <m.killer@langui.ch>

'''
import unittest
from nose.tools import *  # PEP8 asserts

from textblob_de.parsers import get_kwarg_lemmata, PatternParser
from textblob_de.tokenizers import PatternTokenizer, NLTKPunktTokenizer, get_arg_tokenizer
from textblob_de.de import parse as pattern_parse


class TestPatternParserWithNLTKTok(unittest.TestCase):

    def setUp(self):
        self.tokenizer = NLTKPunktTokenizer()
        self.parser = PatternParser()
        self.text = u"Das Auto ist sehr schön."

        self.expected = u"Das/DT/B-NP/O Auto/NN/I-NP/O ist/VB/B-VP/O " \
                        u"sehr/RB/B-ADJP/O schön/JJ/I-ADJP/O ././O/O"

        self.expected_with_lemmata = \
            u'Das/DT/B-NP/O/das Auto/NN/I-NP/O/auto ' \
            u'ist/VB/B-VP/O/sein sehr/RB/B-ADJP/O/sehr ' \
            u'schön/JJ/I-ADJP/O/schön ././O/O/.'

        setattr(get_arg_tokenizer, 'tokenizer', self.tokenizer)
        setattr(get_kwarg_lemmata, "lemmata", False)

    def tearDown(self):
        delattr(get_arg_tokenizer, 'tokenizer')
        delattr(get_kwarg_lemmata, "lemmata")

    def test_parse(self):
        assert_equal(
            self.parser.parse(
                self.text), pattern_parse(
                self.text, self.tokenizer))

    def test_parse_result_string(self):
        assert_equal(self.parser.parse(self.text), self.expected)

    def test_parse_show_lemmata(self):
        setattr(get_kwarg_lemmata, "lemmata", True)
        assert_equal(self.parser.parse(self.text), self.expected_with_lemmata)


class TestPatternParserWithPatternTok(unittest.TestCase):

    def setUp(self):
        self.tokenizer = PatternTokenizer()
        self.parser = PatternParser()
        self.text = u"Das Auto ist sehr schön."
        self.expected = u"Das/DT/B-NP/O Auto/NN/I-NP/O ist/VB/B-VP/O " \
                        u"sehr/RB/B-ADJP/O schön/JJ/I-ADJP/O ././O/O"
        setattr(get_arg_tokenizer, 'tokenizer', self.tokenizer)

    def tearDown(self):
        delattr(get_arg_tokenizer, 'tokenizer')

    def test_parse(self):
        # print(self.parser.parse(self.text))
        assert_equal(
            self.parser.parse(
                self.text), pattern_parse(
                self.text, self.tokenizer))

    def test_parse_result_string(self):
        assert_equal(pattern_parse(self.text, self.tokenizer), self.expected)


if __name__ == '__main__':
    unittest.main()

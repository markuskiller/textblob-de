# -*- coding: utf-8 -*-
'''Code imported from ``textblob`` main package.

:repo: `https://github.com/sloria/TextBlob`_
:source: tests/test_parsers.py
:version: 2013-10-21 (a88e86a76a)

:modified: July 2014 <m.killer@langui.ch>

'''
import unittest
from nose.tools import *  # PEP8 asserts

from textblob_de import PatternParser
from textblob_de.tokenizers import PatternTokenizer, NLTKPunktTokenizer, get_tokenizer
from textblob_de.de import parse as pattern_parse


class TestPatternParserWithNLTKTok(unittest.TestCase):

    def setUp(self):
        self.tokenizer = NLTKPunktTokenizer()
        self.parser = PatternParser()
        self.text = u"Das Auto ist sehr schön."
        self.expected = u"Das/DT/B-NP/O Auto/NN/I-NP/O ist/VB/B-VP/O " \
                        u"sehr/RB/B-ADJP/O schön/JJ/I-ADJP/O ././O/O"
        setattr(get_tokenizer, 'tokenizer', self.tokenizer)
        
    def tearDown(self):
        delattr(get_tokenizer, 'tokenizer')

    def test_parse(self):
        #print(self.parser.parse(self.text))
        assert_equal(self.parser.parse(self.text), pattern_parse(self.text, self.tokenizer))

    def test_parse_result_string(self):
        assert_equal(pattern_parse(self.text, self.tokenizer), self.expected)
        
        
class TestPatternParserWithPatternTok(unittest.TestCase):

    def setUp(self):
        self.tokenizer = PatternTokenizer()
        self.parser = PatternParser()
        self.text = u"Das Auto ist sehr schön."
        self.expected = u"Das/DT/B-NP/O Auto/NN/I-NP/O ist/VB/B-VP/O " \
                        u"sehr/RB/B-ADJP/O schön/JJ/I-ADJP/O ././O/O"
        setattr(get_tokenizer, 'tokenizer', self.tokenizer)
        
    def tearDown(self):
        delattr(get_tokenizer, 'tokenizer')

    def test_parse(self):
        #print(self.parser.parse(self.text))
        assert_equal(self.parser.parse(self.text), pattern_parse(self.text, self.tokenizer))

    def test_parse_result_string(self):
        assert_equal(pattern_parse(self.text, self.tokenizer), self.expected)


if __name__ == '__main__':
    unittest.main()

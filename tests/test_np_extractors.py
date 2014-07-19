# -*- coding: utf-8 -*-
'''Test cases for np extractors.
'''
from __future__ import unicode_literals
import unittest
from nose.tools import *  # PEP8 asserts

from textblob_de.np_extractors import PatternParserNPExtractor


class TestPatternParserNPExtractor(unittest.TestCase):

    def setUp(self):
        self.extractor = PatternParserNPExtractor()
        self.text = u"Peter hat ein schönes Auto. Er wohnt in Zürich. " \
                    u"Seine zwei Katzen heissen Tim und Struppi."

        self.parsed_sentences_expected = [
            u'Peter/NNP/B-NP/O/peter hat/VB/B-VP/O/haben ein/DT/B-NP/O/ein ' \
            u'schönes/JJ/I-NP/O/schön Auto/NN/I-NP/O/auto ././O/O/.', 
            u'Er/PRP/B-NP/O/er wohnt/NN/I-NP/O/wohnt in/IN/B-PP/B-PNP/in ' \
            u'Zürich/NNP/B-NP/I-PNP/zürich ././O/O/.', 'Seine/PRP$/B-NP/O/seine '\
            u'zwei/CD/I-NP/O/zwei Katzen/NNS/I-NP/O/katze heissen/VB/B-VP/O/heissen '\
            u'Tim/NNP/B-NP/O/tim und/CC/I-NP/O/und Struppi/NNP/I-NP/O/struppi ././O/O/.']

    def test_parse_text(self):
        assert_equal(self.extractor._parse_text(self.text), self.parsed_sentences_expected)
        
    def test_extract(self):
        noun_phrases = self.extractor.extract(self.text)
        assert_true("Peter" in noun_phrases)
        assert_true(u"schönes Auto" in noun_phrases)
        # only words tagged as nouns are capitalized other words are normalised
        assert_true(u"er" in noun_phrases)
        assert_true(u"Zürich" in noun_phrases)
        assert_true(u"Tim und Struppi" in noun_phrases)

if __name__ == '__main__':
    unittest.main()
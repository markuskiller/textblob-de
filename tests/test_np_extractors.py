# -*- coding: utf-8 -*-
"""Test cases for np extractors."""
from __future__ import unicode_literals
import unittest
from nose.tools import *  # PEP8 asserts

from textblob_de import PatternParserNPExtractor, NLTKPunktTokenizer


class TestPatternParserNPExtractor(unittest.TestCase):

    def setUp(self):
        self.extractor = PatternParserNPExtractor(
            tokenizer=NLTKPunktTokenizer())
        self.text = "Peter hat ein schönes Auto. Er wohnt in Zürich. " \
                    "Seine zwei Katzen heissen Tim und Struppi."

        self.parsed_sentences_expected = [
            'Peter/NNP/B-NP/O hat/VB/B-VP/O ein/DT/B-NP/O '
            'schönes/JJ/I-NP/O Auto/NN/I-NP/O ././O/O',
            'Er/PRP/B-NP/O wohnt/NN/I-NP/O in/IN/B-PP/B-PNP '
            'Zürich/NNP/B-NP/I-PNP ././O/O', 'Seine/PRP$/B-NP/O '
            'zwei/CD/I-NP/O Katzen/NNS/I-NP/O heissen/VB/B-VP/O '
            'Tim/NNP/B-NP/O und/CC/I-NP/O Struppi/NNP/I-NP/O ././O/O']

    def test_parse_text(self):
        assert_equal(
            self.extractor._parse_text(
                self.text),
            self.parsed_sentences_expected)

    def test_extract(self):
        noun_phrases = self.extractor.extract(self.text)
        assert_true("Peter" in noun_phrases)
        assert_true("schönes Auto" in noun_phrases)
        # only words tagged as nouns are capitalized other words are normalised
        assert_true("er" in noun_phrases)
        assert_true("Zürich" in noun_phrases)
        # added 'und'/'oder' to noun phrase splitters and insignificant
        assert_false("Tim und Struppi" in noun_phrases)

if __name__ == '__main__':
    unittest.main()

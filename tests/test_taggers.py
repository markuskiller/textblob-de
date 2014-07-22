#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Code imported from ``textblob-fr`` sample extension.

:repo: `https://github.com/sloria/textblob-fr`_
:source: tests/test_taggers.py
:version: 2013-09-18 (1a8438b5ea)

:modified: July 2014 <m.killer@langui.ch>

'''
from __future__ import unicode_literals
import unittest
import logging
from nose.tools import *  # PEP8 asserts

from textblob_de import TextBlobDE as TextBlob
from textblob_de import PatternTokenizer, NLTKPunktTokenizer
from textblob_de import PatternTagger


class TestPatternTagger(unittest.TestCase):

    def setUp(self):
        self.text = "Das ist ein schönes Auto."
        

    def test_tag_nltk_tok(self):
        _tagger = PatternTagger(tokenizer=NLTKPunktTokenizer())
        tags = _tagger.tag(self.text)
        logging.debug("tags: {0}".format(tags))
        words = ["Das", "ist", "ein", "schönes", "Auto"]
        for i, word_tag in enumerate(tags):
            assert_equal(word_tag[0], words[i])

    def test_tag_blob_defaults(self):
        blob = TextBlob(self.text)
        tags = blob.tags
        logging.debug("tags: {0}".format(tags))
        words = ["Das", "ist", "ein", "schönes", "Auto"]
        for i, word_tag in enumerate(tags):
            assert_equal(word_tag[0], words[i])
        assert_equal(tags[-1][0], "Auto")
            
    def test_tag_blob_nltk_tok_include_punc(self):
        blob = TextBlob(self.text, tokenizer=NLTKPunktTokenizer(), 
                        pos_tagger=PatternTagger(include_punc=True))
        tags = blob.tags
        logging.debug("tags: {0}".format(tags))
        words = ["Das", "ist", "ein", "schönes", "Auto", "."]
        for i, word_tag in enumerate(tags):
            assert_equal(word_tag[0], words[i])
        assert_equal(tags[-1][0], ".")

    def test_tag_pattern_defaults(self):
        _tagger = PatternTagger()
        tags = _tagger.tag(self.text)
        logging.debug("tags: {0}".format(tags))
        words = ["Das", "ist", "ein", "schönes", "Auto"]
        for i, word_tag in enumerate(tags):
            assert_equal(word_tag[0], words[i])

    def test_tag_blob_pattern_tok(self):
        blob = TextBlob(self.text, tokenizer=PatternTokenizer(), pos_tagger=PatternTagger())
        tags = blob.tags
        logging.debug("tags: {0}".format(tags))
        words = ["Das", "ist", "ein", "schönes", "Auto"]
        for i, word_tag in enumerate(tags):
            assert_equal(word_tag[0], words[i])
            
    def test_tag_blob_pattern_tok_include_punc(self):
        blob = TextBlob(self.text, tokenizer=PatternTokenizer(), 
                        pos_tagger=PatternTagger(include_punc=True))
        tags = blob.tags
        logging.debug("tags: {0}".format(tags))
        words = ["Das", "ist", "ein", "schönes", "Auto", "."]
        for i, word_tag in enumerate(tags):
            assert_equal(word_tag[0], words[i])


if __name__ == '__main__':
    unittest.main()

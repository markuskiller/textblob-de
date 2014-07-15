#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import logging
from nose.tools import *  # PEP8 asserts

from textblob import TextBlob
from textblob_de import PatternTagger


class TestPatternTagger(unittest.TestCase):

    def setUp(self):
        self.tagger = PatternTagger()
        self.text = u"Das ist ein schönes Auto"

    def test_tag(self):
        tags = self.tagger.tag(self.text)
        logging.debug("tags: {0}".format(tags))
        words = self.text.split()
        for i, word_tag in enumerate(tags):
            assert_equal(word_tag[0], words[i])

    def test_tag_blob(self):
        blob = TextBlob(self.text, pos_tagger=self.tagger)
        tags = blob.tags
        logging.debug("tags: {0}".format(tags))
        words = self.text.split()
        for i, word_tag in enumerate(tags):
            assert_equal(word_tag[0], words[i])


if __name__ == '__main__':
    unittest.main()

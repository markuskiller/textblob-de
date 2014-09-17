# -*- coding: utf-8 -*-
# Code adapted from the main `TextBlob`_ library.
#
# :repo: `https://github.com/sloria/TextBlob`_
# :source: tests/test_tokenizers.py
# :version: 2013-12-27 (73bbcaa693)
#
# :modified: 2014-08-29 <m.killer@langui.ch>
#
"""Test cases for tokenziers."""
from __future__ import unicode_literals
import unittest
from nose.tools import *  # PEP8 asserts

from textblob_de import NLTKPunktTokenizer, PatternTokenizer
from textblob_de.tokenizers import WordTokenizer, word_tokenize
from textblob.compat import PY2


def is_generator(obj):
    if PY2:
        return hasattr(obj, 'next')
    else:
        return hasattr(obj, '__next__')


class TestNLTKPunktTokenizer(unittest.TestCase):

    def setUp(self):
        self.tokenizer = NLTKPunktTokenizer()
        self.text = "Heute ist der 3. Mai 2014 und Dr. Meier feiert seinen 43. " \
            "Geburtstag. Ich muss unbedingt daran denken, Mehl, usw. für " \
            "einen Kuchen einzukaufen. Aber leider habe ich nur noch " \
            "EUR 3.50 in meiner Brieftasche."
        self.snt1 = "Heute ist der 3. Mai 2014 und Dr. Meier feiert seinen 43. " \
            "Geburtstag."

    def tearDown(self):
        pass

    def test_tokenize(self):
        assert_equal(self.tokenizer.tokenize(self.text),
                     ['Heute',
                      'ist',
                      'der',
                      '3.',
                      'Mai',
                      '2014',
                      'und',
                      'Dr.',
                      'Meier',
                      'feiert',
                      'seinen',
                      '43.',
                      'Geburtstag',
                      '.',
                      'Ich',
                      'muss',
                      'unbedingt',
                      'daran',
                      'denken',
                      ',',
                      'Mehl',
                      ',',
                      'usw.',
                      'für',
                      'einen',
                      'Kuchen',
                      'einzukaufen',
                      '.',
                      'Aber',
                      'leider',
                      'habe',
                      'ich',
                      'nur',
                      'noch',
                      'EUR',
                      '3.50',
                      'in',
                      'meiner',
                      'Brieftasche',
                      '.'])

    def test_exclude_punc(self):
        assert_equal(self.tokenizer.tokenize(self.text,
                                             include_punc=False),
                     ['Heute',
                      'ist',
                      'der',
                      '3',
                      'Mai',
                      '2014',
                      'und',
                      'Dr',
                      'Meier',
                      'feiert',
                      'seinen',
                      '43',
                      'Geburtstag',
                      'Ich',
                      'muss',
                      'unbedingt',
                      'daran',
                      'denken',
                      'Mehl',
                      'usw',
                      'für',
                      'einen',
                      'Kuchen',
                      'einzukaufen',
                      'Aber',
                      'leider',
                      'habe',
                      'ich',
                      'nur',
                      'noch',
                      'EUR',
                      '3.50',
                      'in',
                      'meiner',
                      'Brieftasche'])

    def test_tokenize_nested(self):
        assert_equal(self.tokenizer.tokenize(self.text,
                                             nested=True),
                     [['Heute',
                       'ist',
                       'der',
                       '3.',
                       'Mai',
                       '2014',
                       'und',
                       'Dr.',
                       'Meier',
                       'feiert',
                       'seinen',
                       '43.',
                       'Geburtstag',
                       '.'],
                      ['Ich',
                       'muss',
                       'unbedingt',
                       'daran',
                       'denken',
                       ',',
                       'Mehl',
                       ',',
                       'usw.',
                       'für',
                       'einen',
                       'Kuchen',
                       'einzukaufen',
                       '.'],
                      ['Aber',
                       'leider',
                       'habe',
                       'ich',
                       'nur',
                       'noch',
                       'EUR',
                       '3.50',
                       'in',
                       'meiner',
                       'Brieftasche',
                       '.']])

    def test_itokenize(self):
        gen = self.tokenizer.itokenize(self.text)
        assert_true(is_generator(gen))
        assert_equal(next(gen), 'Heute')
        assert_equal(next(gen), 'ist')

    def test_sent_tokenize(self):
        assert_equal(
            self.tokenizer.sent_tokenize(
                self.text),
            [
                'Heute ist der 3. Mai 2014 und Dr. Meier feiert seinen 43. Geburtstag.',
                'Ich muss unbedingt daran denken, Mehl, usw. für einen Kuchen einzukaufen.',
                'Aber leider habe ich nur noch EUR 3.50 in meiner Brieftasche.'])

    def test_word_tokenize(self):
        tokens = self.tokenizer.word_tokenize(self.snt1)
        assert_equal(tokens, ['Heute', 'ist', 'der', '3.', 'Mai', '2014',
                              'und', 'Dr.', 'Meier', 'feiert', 'seinen', '43.',
                              'Geburtstag', '.'])


class TestPatternTokenizer(unittest.TestCase):

    def setUp(self):
        self.tokenizer = PatternTokenizer()
        self.text = "Heute ist der 3. Mai 2014 und Dr. Meier feiert seinen 43. " \
            "Geburtstag."
        self.snt1 = "Heute ist der 3 ."

    def tearDown(self):
        pass

    def test_tokenize(self):
        assert_equal(self.tokenizer.tokenize(self.text),
                     ['Heute',
                      'ist',
                      'der',
                      '3',
                      '.',
                      'Mai',
                      '2014',
                      'und',
                      'Dr.',
                      'Meier',
                      'feiert',
                      'seinen',
                      '43',
                      '.',
                      'Geburtstag',
                      '.'])

    def test_exclude_punc(self):
        assert_equal(self.tokenizer.tokenize(self.text,
                                             include_punc=False),
                     ['Heute',
                      'ist',
                      'der',
                      '3',
                      'Mai',
                      '2014',
                      'und',
                      'Dr',
                      'Meier',
                      'feiert',
                      'seinen',
                      '43',
                      'Geburtstag'])

    def test_tokenize_nested(self):
        assert_equal(self.tokenizer.tokenize(self.text, nested=True),
                     [['Heute', 'ist', 'der', '3', '.'],
                      ['Mai',
                       '2014',
                       'und',
                       'Dr.',
                       'Meier',
                       'feiert',
                       'seinen',
                       '43',
                       '.'],
                      ['Geburtstag', '.']])

    def test_itokenize(self):
        gen = self.tokenizer.itokenize(self.text)
        assert_true(is_generator(gen))
        assert_equal(next(gen), 'Heute')
        assert_equal(next(gen), 'ist')

    def test_sent_tokenize(self):
        sents = self.tokenizer.sent_tokenize(self.text)
        assert_equal(sents, ['Heute ist der 3 .',
                             'Mai 2014 und Dr. Meier feiert seinen 43 .',
                             'Geburtstag .'])

    def test_word_tokenize(self):
        tokens = self.tokenizer.word_tokenize(self.snt1)
        assert_equal(tokens, ['Heute', 'ist', 'der', '3', '.'])


class TestWordTokenizer(unittest.TestCase):

    def setUp(self):
        self.tokenizer = WordTokenizer()
        self.text = "Python ist eine universelle, üblicherweise interpretierte höhere Programmiersprache."

    def tearDown(self):
        pass

    def test_tokenize(self):
        assert_equal(self.tokenizer.tokenize(self.text),
                     ['Python',
                      'ist',
                      'eine',
                      'universelle',
                      ',',
                      'üblicherweise',
                      'interpretierte',
                      'höhere',
                      'Programmiersprache',
                      '.'])

    def test_exclude_punc(self):
        assert_equal(self.tokenizer.tokenize(self.text,
                                             include_punc=False),
                     ['Python',
                      'ist',
                      'eine',
                      'universelle',
                      'üblicherweise',
                      'interpretierte',
                      'höhere',
                      'Programmiersprache'])

    def test_itokenize(self):
        gen = self.tokenizer.itokenize(self.text)
        assert_equal(next(gen), "Python")
        assert_equal(next(gen), "ist")

    def test_word_tokenize(self):
        tokens = word_tokenize(self.text)
        assert_true(is_generator(tokens))
        assert_equal(list(tokens), self.tokenizer.tokenize(self.text))

if __name__ == '__main__':
    unittest.main()

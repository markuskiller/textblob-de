# -*- coding: utf-8 -*-
'''Code imported from ``textblob`` main package.

:repo: `https://github.com/sloria/TextBlob`_
:source: tests/test_tokenizers.py
:version: 2013-12-27 (73bbcaa693)

:modified: July 2014 <m.killer@langui.ch>

'''
import unittest
from nose.plugins.attrib import attr
from nose.tools import *  # PEP8 asserts

from textblob_de import NLTKPunktTokenizer, PatternTokenizer
from textblob.compat import PY2


def is_generator(obj):
    if PY2:
        return hasattr(obj, 'next')
    else:
        return hasattr(obj, '__next__')


class TestNLTKPunktTokenizer(unittest.TestCase):

    def setUp(self):
        self.tokenizer = NLTKPunktTokenizer()
        self.text = u"Heute ist der 3. Mai 2014 und Dr. Meier feiert seinen 43. " \
            u"Geburtstag. Ich muss unbedingt daran denken, Mehl, usw. für " \
            u"einen Kuchen einzukaufen. Aber leider habe ich nur noch " \
            u"EUR 18.50 in meiner Brieftasche."
        self.snt1 = u"Heute ist der 3. Mai 2014 und Dr. Meier feiert seinen 43. " \
            u"Geburtstag."

    def tearDown(self):
        pass

    def test_tokenize(self):
        assert_equal(self.tokenizer.tokenize(self.text),
                     ['Heute', 'ist', 'der', '3.', 'Mai', '2014', 'und', 'Dr.',
                      'Meier', 'feiert', 'seinen', '43.', 'Geburtstag', '.', 'Ich',
                      'muss', 'unbedingt', 'daran', 'denken', ',', 'Mehl', ',',
                      'usw.', u'für', 'einen', 'Kuchen', 'einzukaufen', '.', 'Aber',
                      'leider', 'habe', 'ich', 'nur', 'noch', 'EUR', '18.50', 'in',
                      'meiner', 'Brieftasche', '.'])

    def test_exclude_punc(self):
        assert_equal(self.tokenizer.tokenize(self.text, include_punc=False),
                     ['Heute', 'ist', 'der', '3', 'Mai', '2014', 'und', 'Dr', 'Meier',
                      'feiert', 'seinen', '43', 'Geburtstag', 'Ich', 'muss', 'unbedingt',
                      'daran', 'denken', 'Mehl', 'usw', u'für', 'einen', 'Kuchen',
                      'einzukaufen', 'Aber', 'leider', 'habe', 'ich', 'nur', 'noch',
                      'EUR', '18.50', 'in', 'meiner', 'Brieftasche'])

    def test_tokenize_nested(self):
        assert_equal(self.tokenizer.tokenize(self.text, nested=True),
                     [['Heute', 'ist', 'der', '3.', 'Mai', '2014', 'und', 'Dr.',
                       'Meier', 'feiert', 'seinen', '43.', 'Geburtstag', '.'], ['Ich',
                                                                                'muss', 'unbedingt', 'daran', 'denken', ',', 'Mehl', ',',
                                                                                'usw.', u'für', 'einen', 'Kuchen', 'einzukaufen', '.'], ['Aber',
                                                                                                                                         'leider', 'habe', 'ich', 'nur', 'noch', 'EUR', '18.50', 'in',
                                                                                                                                         'meiner', 'Brieftasche', '.']])

    def test_itokenize(self):
        gen = self.tokenizer.itokenize(self.text)
        assert_true(is_generator(gen))
        assert_equal(next(gen), 'Heute')
        assert_equal(next(gen), 'ist')

    def test_sent_tokenize(self):
        assert_equal(self.tokenizer.sent_tokenize(self.text),
                     [u'Heute ist der 3. Mai 2014 und Dr. Meier feiert seinen 43. Geburtstag.',
                      u'Ich muss unbedingt daran denken, Mehl, usw. für einen Kuchen einzukaufen.',
                      u'Aber leider habe ich nur noch EUR 18.50 in meiner Brieftasche.'])

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
                     ['Heute', 'ist', 'der', '3', '.',
                      'Mai', '2014', 'und', 'Dr.', 'Meier', 'feiert', 'seinen', '43', '.',
                      'Geburtstag', '.'])

    def test_exclude_punc(self):
        assert_equal(self.tokenizer.tokenize(self.text, include_punc=False),
                     ['Heute', 'ist', 'der', '3', 'Mai', '2014', 'und', 'Dr', 'Meier',
                      'feiert', 'seinen', '43', 'Geburtstag'])

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

if __name__ == '__main__':
    unittest.main()

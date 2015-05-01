# -*- coding: utf-8 -*-
# Code imported from the main `TextBlob`_ library.
#
# :repo: `https://github.com/sloria/TextBlob`_
# :source: tests/test_blob.py
# :version: 2014-06-29 (8351166e36)
#
# :modified: 2014-08-03 <m.killer@langui.ch>
#
"""Tests for the text processor."""
from __future__ import unicode_literals

import functools
import json
import nose

from unittest import TestCase, main
from datetime import datetime
from nose.tools import *  # PEP8 asserts
from nose.plugins.attrib import attr

import nltk
import textblob_de as tb

from textblob_de.compat import PY2, unicode, basestring, binary_type
from textblob_de.np_extractors import PatternParserNPExtractor
from textblob_de.taggers import PatternTagger
from textblob_de.tokenizers import WordTokenizer, SentenceTokenizer, NLTKPunktTokenizer
from textblob_de.sentiments import PatternAnalyzer
from textblob_de.parsers import PatternParser
from textblob_de.classifiers import NaiveBayesClassifier

import textblob.wordnet as wn


def expected_failure(test):
    """Decorator for expected failures in nose tests.

    Source [accessed: 21/07/2014]:
    http://stackoverflow.com/questions/9613932/nose-plugin-for-expected-failures

    """
    @functools.wraps(test)
    def inner(*args, **kwargs):
        try:
            test(*args, **kwargs)
        except Exception:
            raise nose.SkipTest
        else:
            raise AssertionError('Failure expected')
    return inner

Synset = nltk.corpus.reader.Synset

# train = [
#('Ich liebe dieses Sandwich.', 'pos'),
#('Dieser Ort ist wunderbar!', 'pos'),
#("Was für ein grossartiges Abendessen.", 'pos'),
#('Ich mag dieses Bier wirklich gut.', 'pos'),
#('Das ist meine beste Leistung bisher.', 'pos'),
#("Was für ein Ausblick!", 'pos'),
#('Ich mag dieses Restaurant nicht.', 'neg'),
#('Ich habe diese Angelegenheit satt!', 'neg'),
#("Ich kann nicht damit umgehen.", 'neg'),
#('Er ist mein Erzfeind!', 'neg'),
#('Mein Vorgesetzter ist schrecklich.', 'neg')
#]

# test = [
#('Das Bier war gut.', 'pos'),
#('Ich mag meine Arbeitsstelle nicht.', 'neg'),
#("I ain't feeling dandy today.", 'neg'),
#("Ich fühle mich wunderbar!", 'pos'),
#('Gary ist ein Freund von mir.', 'pos'),
#("Ich kann nicht glauben, dass ich hier mitmache.", 'neg')
#]

#classifier = NaiveBayesClassifier(train)


class WordListTest(TestCase):

    def setUp(self):
        self.words = 'Schön ist besser als hässlich'.split()
        self.mixed = ['Hund', 'Hunde', 'bellen', 'Blob', 'Text']

    def test_len(self):
        wl = tb.WordList(['Schön', 'ist', 'besser'])
        assert_equal(len(wl), 3)

    def test_slicing(self):
        wl = tb.WordList(self.words)
        first = wl[0]
        assert_true(isinstance(first, tb.Word))
        assert_equal(first, 'Schön')

        dogs = wl[0:2]
        assert_true(isinstance(dogs, tb.WordList))
        assert_equal(dogs, tb.WordList(['Schön', 'ist']))

    def test_repr(self):
        wl = tb.WordList(['Schön', 'ist', 'besser'])
        # This compat clause is necessary because from __future__ import unicode_literals
        # turns the whole second argument into one single unicode string:
        # Without it you get an AssertionError on PY2:
        # "WordList([u'Sch\\xf6n', u'ist', u'besser'])" != \
        # u"WordList(['Sch\xf6n', 'ist', 'besser'])"
        if PY2:
            assert_equal(
                unicode(
                    repr(wl)),
                u"WordList([u'Sch\\xf6n', u'ist', u'besser'])")
        else:
            assert_equal(repr(wl), "WordList(['Schön', 'ist', 'besser'])")

    def test_slice_repr(self):
        wl = tb.WordList(['Schön', 'ist', 'besser'])
        if PY2:
            assert_equal(unicode(repr(wl[:2])),
                         u"WordList([u'Sch\\xf6n', u'ist'])")
        else:
            assert_equal(repr(wl[:2]), "WordList(['Schön', 'ist'])")

    def test_str(self):
        wl = tb.WordList(self.words)
        assert_equal(str(wl), str(self.words))

    def test_singularize(self):
        wl = tb.WordList(['Hunde', 'Katzen', 'Büffel',
                          # 'Menschen', 'Mäuse' not processed correctly
                          ])
        assert_equal(wl.singularize(), tb.WordList(['Hund', 'Katze', 'Büffel',
                                                    # 'Mensch', 'Maus' processed as
                                                    # 'Menschen', 'Mäus'
                                                    ]))

    def test_pluralize(self):
        wl = tb.WordList(['Hund', 'Katze', 'Büffel'])
        assert_equal(
            wl.pluralize(), tb.WordList(['Hunde', 'Katzen', 'Büffel']))

    #@attr('slow')
    @expected_failure
    def test_lemmatize(self):
        wl = tb.WordList(["Katze", "Hunde", "Ochsen"])
        assert_equal(wl.lemmatize(), tb.WordList(['Katze', 'Hund', 'Ochse']))

    def test_upper(self):
        wl = tb.WordList(self.words)
        assert_equal(wl.upper(), tb.WordList([w.upper() for w in self.words]))

    def test_lower(self):
        wl = tb.WordList(['Philosophie', 'voN', 'PYTHON'])
        assert_equal(wl.lower(), tb.WordList(['philosophie', 'von', 'python']))

    def test_count(self):
        wl = tb.WordList(['monty', 'python', 'Python', 'Monty'])
        assert_equal(wl.count('monty'), 2)
        assert_equal(wl.count('monty', case_sensitive=True), 1)
        assert_equal(wl.count('mon'), 0)

    def test_convert_to_list(self):
        wl = tb.WordList(self.words)
        assert_equal(list(wl), self.words)

    def test_append(self):
        wl = tb.WordList(['Hund'])
        wl.append("Katze")
        assert_true(isinstance(wl[1], tb.Word))
        wl.append(('ein', 'Tupel'))
        assert_true(isinstance(wl[2], tuple))

    def test_extend(self):
        wl = tb.WordList(["Hunde", "Katzen"])
        wl.extend(["Büffel", 4])
        assert_true(isinstance(wl[2], tb.Word))
        assert_true(isinstance(wl[3], int))


class SentenceTest(TestCase):

    def setUp(self):
        self.empty_sentence = tb.Sentence(" ")
        self.single_period = tb.Sentence(" .")
        self.single_comma = tb.Sentence(" ,")
        self.text_space_period = tb.Sentence("A .")
        self.single_exclamation_mark = tb.Sentence(" !  ")
        self.raw_sentence = \
            'Peter mag Restaurants, die belgisches Bier servieren.'
        self.sentence = tb.Sentence(self.raw_sentence)

    def test_empty_sentence(self):
        assert_equal(self.empty_sentence.tags, [])
        assert_equal(self.empty_sentence.tokens, tb.WordList([]))
        assert_equal(self.empty_sentence.words, tb.WordList([]))
        assert_equal(self.empty_sentence.noun_phrases, tb.WordList([]))
        assert_equal(self.empty_sentence.np_counts, {})
        assert_equal(self.empty_sentence.word_counts, {})
        assert_equal(self.empty_sentence.ngrams(), [])
        assert_equal(self.empty_sentence.parse(), "")

    def test_single_punctuation(self):
        assert_equal(self.single_period.tags, [])
        assert_equal(self.single_period.parse(), "././O/O")
        assert_equal(self.single_comma.parse(), ",/,/O/O")
        assert_equal(self.single_exclamation_mark.parse(), "!/./O/O")

    def test_text_space_period(self):
        assert_equal(self.text_space_period.tokens, ['A', '.'])

    def test_repr(self):
        # In Py2, repr returns bytestring
        if PY2:
            assert_equal(
                repr(
                    self.sentence), b"Sentence(\"{0}\")".format(
                    binary_type(
                        self.raw_sentence)))
        # In Py3, returns text type string
        else:
            assert_equal(
                repr(
                    self.sentence), 'Sentence("{0}")'.format(
                    self.raw_sentence))

    def test_stripped_sentence(self):
        assert_equal(self.sentence.stripped,
                     'peter mag restaurants die belgisches bier servieren')

    def test_len(self):
        assert_equal(len(self.sentence), len(self.raw_sentence))

    @attr('slow')
    def test_dict(self):
        sentence_dict = self.sentence.dict
        assert_equal(sentence_dict, {
            'raw': self.raw_sentence,
            'start_index': 0,
            'polarity': 1.0,
            'subjectivity': 0.0,
            'end_index': len(self.raw_sentence) - 1,
            'stripped': 'peter mag restaurants die belgisches bier servieren',
            'noun_phrases': self.sentence.noun_phrases,
        })

    def test_pos_tags(self):
        then1 = datetime.now()

        tagged = self.sentence.pos_tags
        now1 = datetime.now()
        t1 = now1 - then1

        then2 = datetime.now()
        tagged = self.sentence.pos_tags
        now2 = datetime.now()
        t2 = now2 - then2

        # Getting the pos tags the second time should be faster
        # because they were stored as an attribute the first time
        print("T1, T2 ", t1, t2)
        assert_true(t2 < t1)
        assert_equal(tagged,

                     [('Peter', 'NNP'), ('mag', 'VB'), ('Restaurants', 'NN'),
                      ('die', 'DT'), ('belgisches', 'JJ'), ('Bier', 'NN'), ('servieren', 'VB')]

                     )

    @attr('slow')
    def test_noun_phrases(self):
        nps = self.sentence.noun_phrases
        assert_equal(nps, ['belgisches Bier'])

    def test_words_are_word_objects(self):
        words = self.sentence.words
        assert_true(isinstance(words[0], tb.Word))
        #assert_equal(words[1].pluralize(), 'places')

    def test_string_equality(self):
        assert_equal(
            self.sentence,
            'Peter mag Restaurants, die belgisches Bier servieren.')

    @attr("requires_internet")
    def test_translate(self):
        blob = tb.Sentence("Das ist ein Satz.")
        assert_true(isinstance(blob.tokenizer, NLTKPunktTokenizer))
        translated = blob.translate(to="en")
        assert_true(isinstance(translated, tb.Sentence))
        # For some languages punctuation gets separated for others
        # it does not (not entirely sure if this is Google or TextBlob)
        # Further tests needed.
        assert_equal(translated, "This is a sentence .")

    @expected_failure
    def test_correct(self):
        blob = tb.Sentence("Meinne Reschtschreibung ist schrrecklich.")
        assert_true(isinstance(blob.correct(), tb.Sentence))
        assert_equal(
            blob.correct(),
            tb.Sentence("Meine Rechtschreibung ist schrecklich."))
        blob = tb.Sentence("Meinne Reschtschreibung \nist guut.")
        assert_true(isinstance(blob.correct(), tb.Sentence))
        assert_equal(
            blob.correct(),
            tb.Sentence("Meine Rechtschreibung \nist gut."))

    @attr('requires_internet')
    def test_translate_detects_language_by_default(self):
        blob = tb.TextBlobDE(unicode("ذات سيادة كاملة"))
        assert_true(blob.translate() in ("Vollständig souveränen",
                                         "Mit voller Souveränität",
                                         "Mit vollen Souveränität"))


# class TextBlobTest(TestCase):

    # def setUp(self):
        # self.text = \
        #"""Beautiful is better than ugly.
# Explicit is better than implicit.
# Simple is better than complex.
# Complex is better than complicated.
# Flat is better than nested.
# Sparse is better than dense.
# Readability counts.
# Special cases aren't special enough to break the rules.
# Although practicality beats purity.
# Errors should never pass silently.
# Unless explicitly silenced.
# In the face of ambiguity, refuse the temptation to guess.
# There should be one-- and preferably only one --obvious way to do it.
# Although that way may not be obvious at first unless you're Dutch.
# Now is better than never.
# Although never is often better than *right* now.
# If the implementation is hard to explain, it's a bad idea.
# If the implementation is easy to explain, it may be a good idea.
# Namespaces are one honking great idea -- let's do more of those!"""
        #self.blob = tb.TextBlobDE(self.text)

        # self.np_test_text = '''
# Python is a widely used general-purpose, high-level programming language.
# Its design philosophy emphasizes code readability, and its syntax allows
# programmers to express concepts in fewer
# lines of code than would be possible in languages such as C.
# The language provides constructs intended to enable clear programs on both a small and
# large scale.
# Python supports multiple programming paradigms, including object-oriented,
# imperative and functional programming or procedural styles.
# It features a dynamic type system and automatic memory management and
# has a large and comprehensive standard library. Like other dynamic languages, Python is often
# used as a scripting language,
# but is also used in a wide range of non-scripting contexts.
# Using third-party tools, Python code can be packaged into standalone executable
# programs. Python interpreters are available for many operating systems. CPython, the reference
# implementation of Python, is free and open source software and h
# as a community-based development model, as do nearly all of its alternative implementations.
# CPython is managed by the non-profit Python Software Foundation.'''

        #self.np_test_blob = tb.TextBlobDE(self.np_test_text)

        #self.short = "Beautiful is better than ugly. "
        #self.short_blob = tb.TextBlobDE(self.short)

    # def test_init(self):
        #blob = tb.TextBlobDE('Wow I love this place. It really rocks my socks!')
        #assert_equal(len(blob.sentences), 2)
        #assert_equal(blob.sentences[1].stripped, 'it really rocks my socks')
        #assert_equal(blob.string, blob.raw)

        # Must initialize with a string
        #assert_raises(TypeError, tb.TextBlobDE.__init__, ['invalid'])

    # def test_string_equality(self):
        #blob = tb.TextBlobDE("Textblobs should be equal to strings.")
        #assert_equal(blob, "Textblobs should be equal to strings.")

    # def test_string_comparison(self):
        #blob = tb.TextBlobDE("apple")
        #assert_true(blob < "banana")
        #assert_true(blob > 'aardvark')

    # def test_hash(self):
        #blob = tb.TextBlobDE('apple')
        #assert_equal(hash(blob), hash('apple'))
        #assert_not_equal(hash(blob), hash('banana'))

    # def test_stripped(self):
        #blob = tb.TextBlobDE("Um... well this ain't right.!..")
        #assert_equal(blob.stripped, "um well this aint right")

    # def test_ngrams(self):
        #blob = tb.TextBlobDE("I am eating a pizza.")
        #three_grams = blob.ngrams()
        # assert_equal(three_grams, [
        #tb.WordList(('I', 'am', 'eating')),
        #tb.WordList(('am', 'eating', 'a')),
        #tb.WordList(('eating', 'a', 'pizza'))
        #])
        #four_grams = blob.ngrams(n=4)
        # assert_equal(four_grams, [
        #tb.WordList(('I', 'am', 'eating', 'a')),
        #tb.WordList(('am', 'eating', 'a', 'pizza'))
        #])

    # def test_sentences(self):
        #blob = self.blob
        #assert_equal(len(blob.sentences), 19)
        #assert_true(isinstance(blob.sentences[0], tb.Sentence))

    # def test_senences_with_space_before_punctuation(self):
        #text = "Uh oh. This sentence might cause some problems. : Now we're ok."
        #b = tb.TextBlobDE(text)
        #assert_equal(len(b.sentences), 3)

    # def test_sentiment_of_foreign_text(self):
        # blob = tb.TextBlobDE(u'Nous avons cherch\xe9 un motel dans la r\xe9gion de '
        #'Madison, mais les motels ne sont pas nombreux et nous avons '
        #'finalement choisi un Motel 6, attir\xe9s par le bas '
        #'prix de la chambre.')
        #assert_true(isinstance(blob.sentiment[0], float))

    # def test_iter(self):
        # for i, letter in enumerate(self.short_blob):
        #assert_equal(letter, self.short[i])

    # def test_raw_sentences(self):
        #blob = tb.TextBlobDE(self.text)
        #assert_equal(len(blob.raw_sentences), 19)
        #assert_equal(blob.raw_sentences[0], "Beautiful is better than ugly.")

    # def test_blob_with_no_sentences(self):
        #text = "this isn't really a sentence it's just a long string of words"
        #blob = tb.TextBlobDE(text)
        # the blob just has one sentence
        #assert_equal(len(blob.sentences), 1)
        # the start index is 0, the end index is len(text) - 1
        #assert_equal(blob.sentences[0].start_index, 0)
        #assert_equal(blob.sentences[0].end_index, len(text))

    # def test_len(self):
        #blob = tb.TextBlobDE('lorem ipsum')
        #assert_equal(len(blob), len('lorem ipsum'))

    # def test_repr(self):
        #blob1 = tb.TextBlobDE('lorem ipsum')
        # if PY2:
        #assert_equal(repr(blob1), b"TextBlob(\"{0}\")".format(binary_type('lorem ipsum')))
        # else:
        #assert_equal(repr(blob1), "TextBlob(\"{0}\")".format('lorem ipsum'))

    # def test_cmp(self):
        #blob1 = tb.TextBlobDE('lorem ipsum')
        #blob2 = tb.TextBlobDE('lorem ipsum')
        #blob3 = tb.TextBlobDE('dolor sit amet')

        # assert_true(blob1 == blob2)  # test ==
        # assert_true(blob1 > blob3)  # test >
        # assert_true(blob1 >= blob3)  # test >=
        # assert_true(blob3 < blob2)  # test <
        # assert_true(blob3 <= blob2)  # test <=

    # def test_invalid_comparison(self):
        #blob = tb.TextBlobDE("one")
        # if PY2:
        # invalid comparison returns False
        #assert_false(blob < 2)
        # else:
        # invalid comparison raises Error
        # with assert_raises(TypeError):
        #blob < 2

    # def test_words(self):
        # blob = tb.TextBlobDE('Beautiful is better than ugly. '
        #'Explicit is better than implicit.')
        #assert_true(isinstance(blob.words, tb.WordList))
        # assert_equal(blob.words, tb.WordList([
        #'Beautiful',
        #'is',
        #'better',
        #'than',
        #'ugly',
        #'Explicit',
        #'is',
        #'better',
        #'than',
        #'implicit',
        #]))
        #short = tb.TextBlobDE("Just a bundle of words")
        # assert_equal(short.words, tb.WordList([
        #'Just', 'a', 'bundle', 'of', 'words'
        #]))

    # def test_words_includes_apostrophes_in_contractions(self):
        #blob = tb.TextBlobDE("Let's test this.")
        #assert_equal(blob.words, tb.WordList(['Let', "'s", "test", "this"]))
        #blob2 = tb.TextBlobDE("I can't believe it's not butter.")
        # assert_equal(blob2.words, tb.WordList(['I', 'ca', "n't", "believe",
        #'it', "'s", "not", "butter"]))

    # def test_pos_tags(self):
        # blob = tb.TextBlobDE('Simple is better than complex. '
        #'Complex is better than complicated.')
        # assert_equal(blob.pos_tags, [
        #('Simple', 'JJ'),
        #('is', 'VBZ'),
        #('better', 'JJR'),
        #('than', 'IN'),
        #('complex', 'JJ'),
        #('Complex', 'NNP'),
        #('is', 'VBZ'),
        #('better', 'JJR'),
        #('than', 'IN'),
        #('complicated', 'VBN'),
        #])

    # def test_tags(self):
        #assert_equal(self.blob.tags, self.blob.pos_tags)

    # def test_tagging_nonascii(self):
        # b = tb.TextBlobDE('Learn how to make the five classic French mother sauces: '
        #'Béchamel, Tomato Sauce, Espagnole, Velouté and Hollandaise.')
        #tags = b.tags
        #assert_true(isinstance(tags[0][0], unicode))

    # def test_pos_tags_includes_one_letter_articles(self):
        #blob = tb.TextBlobDE("This is a sentence.")
        #assert_equal(blob.pos_tags[2][0], 'a')

    #@attr('slow')
    # def test_np_extractor_defaults_to_fast_tagger(self):
        #text = "Python is a high-level scripting language."
        #blob1 = tb.TextBlobDE(text)
        #assert_true(isinstance(blob1.np_extractor, FastNPExtractor))

    # def test_np_extractor_is_shared_among_instances(self):
        #blob1 = tb.TextBlobDE("This is one sentence")
        #blob2 = tb.TextBlobDE("This is another sentence")
        #assert_true(blob1.np_extractor is blob2.np_extractor)

    #@attr('slow')
    # def test_can_use_different_np_extractors(self):
        #e = ConllExtractor()
        #text = "Python is a high-level scripting language."
        #blob = tb.TextBlobDE(text)
        #blob.np_extractor = e
        #assert_true(isinstance(blob.np_extractor, ConllExtractor))

    # def test_can_use_different_sentanalyzer(self):
        #blob = tb.TextBlobDE("I love this car", analyzer=NaiveBayesAnalyzer())
        #assert_true(isinstance(blob.analyzer, NaiveBayesAnalyzer))

    #@attr("slow")
    # def test_discrete_sentiment(self):
        #blob = tb.TextBlobDE("I feel great today.", analyzer=NaiveBayesAnalyzer())
        #assert_equal(blob.sentiment[0], 'pos')

    # def test_can_get_subjectivity_and_polarity_with_different_analyzer(self):
        #blob = tb.TextBlobDE("I love this car.", analyzer=NaiveBayesAnalyzer())
        #pattern = PatternAnalyzer()
        #assert_equal(blob.polarity, pattern.analyze(str(blob))[0])
        #assert_equal(blob.subjectivity, pattern.analyze(str(blob))[1])

    # def test_pos_tagger_defaults_to_pattern(self):
        #blob = tb.TextBlobDE("some text")
        #assert_true(isinstance(blob.pos_tagger, PatternTagger))

    # def test_pos_tagger_is_shared_among_instances(self):
        #blob1 = tb.TextBlobDE("This is one sentence")
        #blob2 = tb.TextBlobDE("This is another sentence.")
        #assert_true(blob1.pos_tagger is blob2.pos_tagger)

    # def test_can_use_different_pos_tagger(self):
        #tagger = NLTKTagger()
        #blob = tb.TextBlobDE("this is some text", pos_tagger=tagger)
        #assert_true(isinstance(blob.pos_tagger, NLTKTagger))

    #@attr('slow')
    # def test_can_pass_np_extractor_to_constructor(self):
        #e = ConllExtractor()
        #blob = tb.TextBlobDE('Hello world!', np_extractor=e)
        #assert_true(isinstance(blob.np_extractor, ConllExtractor))

    # def test_getitem(self):
        #blob = tb.TextBlobDE('lorem ipsum')
        #assert_equal(blob[0], 'l')
        #assert_equal(blob[0:5], tb.TextBlobDE('lorem'))

    # def test_upper(self):
        #blob = tb.TextBlobDE('lorem ipsum')
        # assert_true(is_blob(blob.upper()))
        #assert_equal(blob.upper(), tb.TextBlobDE('LOREM IPSUM'))

    # def test_upper_and_words(self):
        #blob = tb.TextBlobDE('beautiful is better')
        # assert_equal(blob.upper().words, tb.WordList(['BEAUTIFUL', 'IS', 'BETTER'
        #]))

    # def test_lower(self):
        #blob = tb.TextBlobDE('Lorem Ipsum')
        # assert_true(is_blob(blob.lower()))
        #assert_equal(blob.lower(), tb.TextBlobDE('lorem ipsum'))

    # def test_find(self):
        #text = 'Beautiful is better than ugly.'
        #blob = tb.TextBlobDE(text)
        # assert_equal(blob.find('better', 5, len(blob)), text.find('better', 5,
        # len(text)))

    # def test_rfind(self):
        #text = 'Beautiful is better than ugly. '
        #blob = tb.TextBlobDE(text)
        #assert_equal(blob.rfind('better'), text.rfind('better'))

    # def test_startswith(self):
        #blob = tb.TextBlobDE(self.text)
        # assert_true(blob.startswith('Beautiful'))
        # assert_true(blob.starts_with('Beautiful'))

    # def test_endswith(self):
        #blob = tb.TextBlobDE(self.text)
        #assert_true(blob.endswith('of those!'))
        #assert_true(blob.ends_with('of those!'))

    # def test_split(self):
        #blob = tb.TextBlobDE('Beautiful is better')
        #assert_equal(blob.split(), tb.WordList(['Beautiful', 'is', 'better']))

    # def test_title(self):
        #blob = tb.TextBlobDE('Beautiful is better')
        #assert_equal(blob.title(), tb.TextBlobDE('Beautiful Is Better'))

    # def test_format(self):
        #blob = tb.TextBlobDE('1 + 1 = {0}')
        #assert_equal(blob.format(1 + 1), tb.TextBlobDE('1 + 1 = 2'))
        #assert_equal('1 + 1 = {0}'.format(tb.TextBlobDE('2')), '1 + 1 = 2')

    # def test_using_indices_for_slicing(self):
        #blob = tb.TextBlobDE("Hello world. How do you do?")
        #sent1, sent2 = blob.sentences
        #assert_equal(blob[sent1.start:sent1.end], tb.TextBlobDE(str(sent1)))
        #assert_equal(blob[sent2.start:sent2.end], tb.TextBlobDE(str(sent2)))

    # def test_indices_with_only_one_sentences(self):
        #blob = tb.TextBlobDE("Hello world.")
        #sent1 = blob.sentences[0]
        #assert_equal(blob[sent1.start:sent1.end], tb.TextBlobDE(str(sent1)))

    # def test_indices_with_multiple_puncutations(self):
        #blob = tb.TextBlobDE("Hello world. How do you do?! This has an ellipses...")
        #sent1, sent2, sent3 = blob.sentences
        #assert_equal(blob[sent2.start:sent2.end], tb.TextBlobDE("How do you do?!"))
        #assert_equal(blob[sent3.start:sent3.end], tb.TextBlobDE("This has an ellipses..."))

    # def test_indices_short_names(self):
        #blob = tb.TextBlobDE(self.text)
        #last_sentence = blob.sentences[len(blob.sentences) - 1]
        #assert_equal(last_sentence.start, last_sentence.start_index)
        #assert_equal(last_sentence.end, last_sentence.end_index)

    # def test_replace(self):
        #blob = tb.TextBlobDE('textblob is a blobby blob')
        # assert_equal(blob.replace('blob', 'bro'),
        # tb.TextBlobDE('textbro is a broby bro'))
        # assert_equal(blob.replace('blob', 'bro', 1),
        # tb.TextBlobDE('textbro is a blobby blob'))

    # def test_join(self):
        #l = ['explicit', 'is', 'better']
        #wl = tb.WordList(l)
        #assert_equal(tb.TextBlobDE(' ').join(l), tb.TextBlobDE('explicit is better'))
        #assert_equal(tb.TextBlobDE(' ').join(wl), tb.TextBlobDE('explicit is better'))

    #@attr('slow')
    # def test_blob_noun_phrases(self):
        #noun_phrases = self.np_test_blob.noun_phrases
        #assert_true('python' in noun_phrases)
        #assert_true('design philosophy' in noun_phrases)

    # def test_word_counts(self):
        #blob = tb.TextBlobDE('Buffalo buffalo ate my blue buffalo.')
        # assert_equal(dict(blob.word_counts), {
        #'buffalo': 3,
        #'ate': 1,
        #'my': 1,
        #'blue': 1
        #})
        #assert_equal(blob.word_counts['buffalo'], 3)
        #assert_equal(blob.words.count('buffalo'), 3)
        #assert_equal(blob.words.count('buffalo', case_sensitive=True), 2)
        #assert_equal(blob.word_counts['blue'], 1)
        #assert_equal(blob.words.count('blue'), 1)
        #assert_equal(blob.word_counts['ate'], 1)
        #assert_equal(blob.words.count('ate'), 1)
        #assert_equal(blob.word_counts['buff'], 0)
        #assert_equal(blob.words.count('buff'), 0)

        #blob2 = tb.TextBlobDE(self.text)
        #assert_equal(blob2.words.count('special'), 2)
        #assert_equal(blob2.words.count('special', case_sensitive=True), 1)

    #@attr('slow')
    # def test_np_counts(self):
        # Add some text so that we have a noun phrase that
        # has a frequency greater than 1
        #noun_phrases = self.np_test_blob.noun_phrases
        #assert_equal(noun_phrases.count('python'), 6)
        #assert_equal(self.np_test_blob.np_counts['python'], noun_phrases.count('python'))
        #assert_equal(noun_phrases.count('cpython'), 2)
        #assert_equal(noun_phrases.count('not found'), 0)

    # def test_add(self):
        #blob1 = tb.TextBlobDE('Hello, world! ')
        #blob2 = tb.TextBlobDE('Hola mundo!')
        # Can add two text blobs
        #assert_equal(blob1 + blob2, tb.TextBlobDE('Hello, world! Hola mundo!'))
        # Can also add a string to a tb.TextBlobDE
        # assert_equal(blob1 + 'Hola mundo!',
        # tb.TextBlobDE('Hello, world! Hola mundo!'))
        # Or both
        # assert_equal(blob1 + blob2 + ' Goodbye!',
        # tb.TextBlobDE('Hello, world! Hola mundo! Goodbye!'))

        # operands must be strings
        #assert_raises(TypeError, blob1.__add__, ['hello'])

    # def test_unicode(self):
        #blob = tb.TextBlobDE(self.text)
        #assert_equal(str(blob), str(self.text))

    # def test_strip(self):
        #text = 'Beautiful is better than ugly. '
        #blob = tb.TextBlobDE(text)
        # assert_true(is_blob(blob))
        #assert_equal(blob.strip(), tb.TextBlobDE(text.strip()))

    # def test_strip_and_words(self):
        #blob = tb.TextBlobDE('Beautiful is better! ')
        # assert_equal(blob.strip().words, tb.WordList(['Beautiful', 'is', 'better'
        #]))

    # def test_index(self):
        #blob = tb.TextBlobDE(self.text)
        #assert_equal(blob.index('Namespaces'), self.text.index('Namespaces'))

    # def test_sentences_after_concatenation(self):
        #blob1 = tb.TextBlobDE('Beautiful is better than ugly. ')
        #blob2 = tb.TextBlobDE('Explicit is better than implicit.')

        #concatenated = blob1 + blob2
        #assert_equal(len(concatenated.sentences), 2)

    # def test_sentiment(self):
        # positive = tb.TextBlobDE('This is the best, most amazing '
        #'text-processing library ever!')
        #assert_true(positive.sentiment[0] > 0.0)
        #negative = tb.TextBlobDE("bad bad bitches that's my muthufuckin problem.")
        #assert_true(negative.sentiment[0] < 0.0)
        #zen = tb.TextBlobDE(self.text)
        #assert_equal(round(zen.sentiment[0], 1), 0.2)

    # def test_subjectivity(self):
        #positive = tb.TextBlobDE("Oh my god this is so amazing! I'm so happy!")
        #assert_true(isinstance(positive.subjectivity, float))
        #assert_true(positive.subjectivity > 0)

    # def test_polarity(self):
        #positive = tb.TextBlobDE("Oh my god this is so amazing! I'm so happy!")
        #assert_true(isinstance(positive.polarity, float))
        #assert_true(positive.polarity > 0)

    # def test_sentiment_of_emoticons(self):
        #b1 = tb.TextBlobDE("Faces have values =)")
        #b2 = tb.TextBlobDE("Faces have values")
        #assert_true(b1.sentiment[0] > b2.sentiment[0])

    # def test_bad_init(self):
        #assert_raises(TypeError, lambda: tb.TextBlobDE(['bad']))
        # assert_raises(ValueError, lambda: tb.TextBlobDE("this is fine",
        # np_extractor="this is not fine"))
        # assert_raises(ValueError, lambda: tb.TextBlobDE("this is fine",
        # pos_tagger="this is not fine"))

    # def test_in(self):
        #blob = tb.TextBlobDE('Beautiful is better than ugly. ')
        #assert_true('better' in blob)
        #assert_true('fugly' not in blob)

    #@attr('slow')
    # def test_json(self):
        #blob = tb.TextBlobDE('Beautiful is better than ugly. ')
        #assert_equal(blob.json, blob.to_json())
        #blob_dict = json.loads(blob.json)[0]
        #assert_equal(blob_dict['stripped'], 'beautiful is better than ugly')
        #assert_equal(blob_dict['noun_phrases'], blob.sentences[0].noun_phrases)
        #assert_equal(blob_dict['start_index'], blob.sentences[0].start)
        #assert_equal(blob_dict['end_index'], blob.sentences[0].end)
        # assert_almost_equal(blob_dict['polarity'],
        # blob.sentences[0].polarity, places=4)
        # assert_almost_equal(blob_dict['subjectivity'],
        # blob.sentences[0].subjectivity, places=4)

    # def test_words_are_word_objects(self):
        #words = self.blob.words
        #assert_true(isinstance(words[0], tb.Word))

    # def test_words_have_pos_tags(self):
        # blob = tb.TextBlobDE('Simple is better than complex. '
        #'Complex is better than complicated.')
        #first_word, first_tag = blob.pos_tags[0]
        #assert_true(isinstance(first_word, tb.Word))
        #assert_equal(first_word.pos_tag, first_tag)

    # def test_tokenizer_defaults_to_word_tokenizer(self):
        #assert_true(isinstance(self.blob.tokenizer, WordTokenizer))

    # def test_tokens_property(self):
        # assert_true(self.blob.tokens,
        # tb.WordList(WordTokenizer().tokenize(self.text)))

    # def test_can_use_an_different_tokenizer(self):
        #tokenizer = nltk.tokenize.TabTokenizer()
        #blob = tb.TextBlobDE("This is\ttext.", tokenizer=tokenizer)
        #assert_equal(blob.tokens, tb.WordList(["This is", "text."]))

    # def test_tokenize_method(self):
        #tokenizer = nltk.tokenize.TabTokenizer()
        #blob = tb.TextBlobDE("This is\ttext.")
        # If called without arguments, should default to WordTokenizer
        #assert_equal(blob.tokenize(), tb.WordList(["This", "is", "text", "."]))
        # Pass in the TabTokenizer
        #assert_equal(blob.tokenize(tokenizer), tb.WordList(["This is", "text."]))

    #@attr("requires_internet")
    # def test_translate(self):
        #blob = tb.TextBlobDE("This is a sentence.")
        #translated = blob.translate(to="es")
        #assert_true(isinstance(translated, tb.TextBlobDE))
        #assert_equal(translated, "Esta es una frase.")
        #es_blob = tb.TextBlobDE("Esta es una frase.")
        #to_en = es_blob.translate(from_lang="es", to="en")
        #assert_equal(to_en, "This is a sentence.")

    #@attr("requires_internet")
    # def test_translate_non_ascii(self):
        #blob = tb.TextBlobDE(unicode("ذات سيادة كاملة"))
        #translated = blob.translate(from_lang="ar", to="en")
        #assert_equal(translated, "With full sovereignty")

        #chinese_blob = tb.TextBlobDE(unicode("美丽优于丑陋"))
        #translated = chinese_blob.translate(from_lang="zh-CN", to='en')
        #assert_equal(translated, "Beautiful is better than ugly")

    #@attr("requires_internet")
    # def test_translate_unicode_escape(self):
        #blob = tb.TextBlobDE("Jenner & Block LLP")
        #translated = blob.translate(from_lang="en", to="en")
        #assert_equal(translated, "Jenner & Block LLP")

    #@attr("requires_internet")
    # def test_detect(self):
        #es_blob = tb.TextBlobDE("Hola")
        #assert_equal(es_blob.detect_language(), "es")
        #en_blob = tb.TextBlobDE("Hello")
        #assert_equal(en_blob.detect_language(), "en")

    #@attr("requires_internet")
    # def test_detect_non_ascii(self):
        #blob = tb.TextBlobDE(unicode("ذات سيادة كاملة"))
        #assert_equal(blob.detect_language(), "ar")

    # def test_correct(self):
        #blob = tb.TextBlobDE("I havv bad speling.")
        #assert_true(isinstance(blob.correct(), tb.TextBlobDE))
        #assert_equal(blob.correct(), tb.TextBlobDE("I have bad spelling."))
        #blob2 = tb.TextBlobDE("I am so exciited!!!")
        #assert_equal(blob2.correct(), "I am so excited!!!")
        #blob3 = tb.TextBlobDE("The meaning of life is 42.0.")
        #assert_equal(blob3.correct(), "The meaning of life is 42.0.")
        #blob4 = tb.TextBlobDE("?")
        #assert_equal(blob4.correct(), "?")
        # From a user-submitted bug
        # text = "Before you embark on any of this journey, write a quick " + \
        #"high-level test that demonstrates the slowness. " + \
        #"You may need to introduce some minimum set of data to " + \
        #"reproduce a significant enough slowness."
        #blob5 = tb.TextBlobDE(text)
        #assert_equal(blob5.correct(), text)
        # text = "Word list!  :\n" + \
        #"\t* spelling\n" + \
        #"\t* well"
        #blob6 = tb.TextBlobDE(text)
        #assert_equal(blob6.correct(), text)

    # def test_parse(self):
        #blob = tb.TextBlobDE("And now for something completely different.")
        #assert_equal(blob.parse(), PatternParser().parse(blob.string))

    # def test_passing_bad_init_params(self):
        #tagger = PatternTagger()
        # assert_raises(ValueError,
        # lambda: tb.TextBlobDE("blah", parser=tagger))
        # assert_raises(ValueError,
        # lambda: tb.TextBlobDE("blah", np_extractor=tagger))
        # assert_raises(ValueError,
        # lambda: tb.TextBlobDE("blah", tokenizer=tagger))
        # assert_raises(ValueError,
        # lambda: tb.TextBlobDE("blah", analyzer=tagger))
        #analyzer = PatternAnalyzer
        # assert_raises(ValueError,
        # lambda: tb.TextBlobDE("blah", pos_tagger=analyzer))

    # def test_classify(self):
        # blob = tb.TextBlobDE("This is an amazing library. What an awesome classifier!",
        # classifier=classifier)
        #assert_equal(blob.classify(), 'pos')
        # for s in blob.sentences:
        #assert_equal(s.classify(), 'pos')

    # def test_classify_without_classifier(self):
        #blob = tb.TextBlobDE("This isn't gonna be good")
        # assert_raises(NameError,
        # lambda: blob.classify())


class WordTest(TestCase):

    def setUp(self):
        self.cat = tb.Word('Katze')
        self.cats = tb.Word('Katzen')

    def test_init(self):
        tb.Word("Katze")
        assert_true(isinstance(self.cat, tb.Word))
        word = tb.Word('Katze', 'NN')
        assert_equal(word.pos_tag, 'NN')

    def test_singularize(self):
        singular = self.cats.singularize()
        assert_equal(singular, 'Katze')
        # Error in pattern.de.inflect (correct: 'Katze')
        assert_equal(self.cat.singularize(), 'Katz')
        assert_true(isinstance(self.cat.singularize(), tb.Word))

    def test_pluralize(self):
        plural = self.cat.pluralize()
        assert_equal(self.cat.pluralize(), 'Katzen')
        assert_true(isinstance(plural, tb.Word))

    def test_repr(self):
        assert_equal(repr(self.cat), repr("Katze"))

    def test_str(self):
        assert_equal(str(self.cat), 'Katze')

    def test_has_str_methods(self):
        assert_equal(self.cat.upper(), "KATZE")
        assert_equal(self.cat.lower(), "katze")
        assert_equal(self.cat[0:2], 'Ka')

    @attr('requires_internet')
    def test_translate(self):
        assert_equal(
            tb.Word("Katze").translate(
                from_lang="de",
                to="en"),
            "cat")

    @attr('requires_internet')
    def test_translate_without_from_lang(self):
        valid_translations = (tb.Word('Hallo'), tb.Word('hallo'),
                              tb.Word('Hallo zusammen'))
        assert_true(tb.Word('Hello').translate() in valid_translations)

    @attr('requires_internet')
    def test_detect_language(self):
        assert_equal(tb.Word("Guten Tag").detect_language(), 'de')

    @expected_failure
    def test_spellcheck(self):
        blob = tb.Word("Reschtschreibung")
        suggestions = blob.spellcheck()
        assert_equal(suggestions[0][0], "Rechtschreibung")

    @expected_failure
    def test_spellcheck_special_cases(self):
        # Punctuation
        assert_equal(tb.Word("!").spellcheck(), [("!", 1.0)])
        # Numbers
        assert_equal(tb.Word("42").spellcheck(), [("42", 1.0)])
        assert_equal(tb.Word("12.34").spellcheck(), [("12.34", 1.0)])
        # One-letter words
        assert_equal(tb.Word("I").spellcheck(), [("I", 1.0)])
        assert_equal(tb.Word("A").spellcheck(), [("A", 1.0)])
        assert_equal(tb.Word("a").spellcheck(), [("a", 1.0)])

    @expected_failure
    def test_correct(self):
        w = tb.Word('Reschtschreibung')
        correct = w.correct()
        assert_equal(correct, tb.Word('Rechtschreibung'))
        assert_true(isinstance(correct, tb.Word))

    @expected_failure
    @attr('slow')
    def test_lemmatize(self):
        w = tb.Word("Autos")
        assert_equal(w.lemmatize(), "Auto")
        w = tb.Word("Wölfe")
        assert_equal(w.lemmatize(), "Wolf")
        w = tb.Word("ging")
        assert_equal(w.lemmatize("v"), "gehen")

    @expected_failure
    def test_lemma(self):
        w = tb.Word("Häuser")
        assert_equal(w.lemma, "Haus")
        w = tb.Word("ging", "VBD")
        assert_equal(w.lemma, "gehen")

    @expected_failure
    def test_synsets(self):
        w = tb.Word("Fahrrad")
        assert_true(isinstance(w.synsets, (list, tuple)))
        assert_true(isinstance(w.synsets[0], Synset))

    @expected_failure
    def test_synsets_with_pos_argument(self):
        w = tb.Word("Arbeit")
        noun_syns = w.get_synsets(pos=wn.NOUN)
        assert_true(len(noun_syns) > 0)
        for synset in noun_syns:
            assert_equal(synset.pos, wn.NOUN)

    @expected_failure
    def test_definitions(self):
        w = tb.Word("Krake")
        assert_true(len(w.definitions) > 0)
        for definition in w.definitions:
            assert_true(isinstance(definition, basestring))

    @expected_failure
    def test_define(self):
        w = tb.Word("Gewinn")
        synsets = w.get_synsets(wn.NOUN)
        definitions = w.define(wn.NOUN)
        assert_true(len(definitions) > 0)
        assert_equal(len(synsets), len(definitions))


# class TestWordnetInterface(TestCase):

    # def setUp(self):
        # pass

    # def test_synset(self):
        #syn = wn.Synset("dog.n.01")
        #word = tb.Word("dog")
        #assert_equal(word.synsets[0], syn)

    # def test_lemma(self):
        #lemma = wn.Lemma('eat.v.01.eat')
        #word = tb.Word("eat")
        #assert_equal(word.synsets[0].lemmas[0], lemma)


class BlobberTest(TestCase):

    def setUp(self):
        self.blobber = tb.BlobberDE()  # The default blobber

    def test_creates_blobs(self):
        blob1 = self.blobber("Das ist ein Blob")
        assert_true(isinstance(blob1, tb.TextBlobDE))
        blob2 = self.blobber("ein anderer Blob")
        assert_equal(blob1.pos_tagger, blob2.pos_tagger)

    def test_default_tagger(self):
        blob = self.blobber("Etwas Text")
        assert_true(isinstance(blob.pos_tagger, PatternTagger))

    def test_default_np_extractor(self):
        blob = self.blobber("Etwas Text")
        assert_true(isinstance(blob.np_extractor, PatternParserNPExtractor))

    def test_default_tokenizer(self):
        blob = self.blobber("Etwas Text")
        assert_true(isinstance(blob.tokenizer, NLTKPunktTokenizer))

    def test_str_and_repr(self):
        expected = "Blobber(tokenizer=NLTKPunktTokenizer(), pos_tagger=PatternTagger(), np_extractor=PatternParserNPExtractor(), analyzer=PatternAnalyzer(), parser=PatternParser(), classifier=None)"
        assert_equal(repr(self.blobber), expected)
        assert_equal(str(self.blobber), repr(self.blobber))

    def test_overrides(self):
        b = tb.BlobberDE(tokenizer=SentenceTokenizer())
        blob = b("Was nun? Dumme Kuh?")
        assert_true(isinstance(blob.tokenizer, SentenceTokenizer))
        assert_equal(blob.tokens, tb.WordList(["Was nun?", "Dumme Kuh?"]))
        blob2 = b("Ein anderer Blob")
        # blobs have the same tokenizer
        assert_true(blob.tokenizer is blob2.tokenizer)
        # but aren't the same object
        assert_not_equal(blob, blob2)

    @expected_failure
    def test_override_analyzer(self):
        b = tb.BlobberDE(analyzer=NaiveBayesAnalyzer())
        blob = b("How now?")
        blob2 = b("Brown cow")
        assert_true(isinstance(blob.analyzer, NaiveBayesAnalyzer))
        assert_true(blob.analyzer is blob2.analyzer)

    @expected_failure
    def test_overrider_classifier(self):
        b = tb.BlobberDE(classifier=classifier)
        blob = b("I am so amazing")
        assert_equal(blob.classify(), 'pos')


def is_blob(obj):
    return isinstance(obj, tb.TextBlobDE)

if __name__ == '__main__':
    main()

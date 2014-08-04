# -*- coding: utf-8 -*-
'''Various noun phrase extractor implementations.

# :class:`PatternParserNPExtractor() <textblob_de.np_extractors.PatternParserNPExtractor>`.

'''
from __future__ import absolute_import

import os
import re

from itertools import chain
from collections import defaultdict

from textblob.base import BaseNPExtractor
from textblob_de.packages import pattern_de
from textblob_de.tokenizers import PatternTokenizer

pattern_parse = pattern_de.parse
Verbs = pattern_de.inflect.Verbs
verbs = pattern_de.inflect.verbs

try:
    MODULE = os.path.dirname(os.path.realpath(__file__))
except:
    MODULE = ""

INSIGNIFICANT = ['der', 'die', 'das', 'des', 'dem', 'ein', 'eine', 'einer', 'einen', 'eines',
                 'welcher', 'welche', 'welches', 'und', 'oder', 'mich', 'dich', 'sich', 'uns', 'euch', 'ihnen']

START_NEW_NP = ['der', 'des', 'und', 'oder']


def _get_verb_lexicon():
    verb_lexicon = defaultdict(set)

    with open(os.path.join(MODULE, 'ext', '_pattern', 'text', 'de', 'de-verbs.txt'), 'r') as _vl:
        for line in _vl:
            verb_lexicon[line[0].lower()] = set(list(verb_lexicon[line[0].lower()])
                                                + line.strip().split(','))

    setattr(_get_verb_lexicon, "cached", verb_lexicon)
    return verb_lexicon


class PatternParserNPExtractor(BaseNPExtractor):

    """Extract noun phrases (NP) from PatternParser() output.

    Very naïve and resource hungry approach:

    * get parser output
    * try to correct as many obvious parser errors as you can (e.g. eliminate wrongly tagged verbs)
    * filter insignificant words

    :param tokenizer: (optional) A tokenizer instance. If ``None``, defaults to
        :class:`PatternTokenizer() <textblob_de.tokenizers.PatternTokenizer>`.
    """

    def __init__(self, tokenizer=None):
        self.tokenizer = tokenizer if tokenizer else PatternTokenizer()
        self.verb_morphology = Verbs()

    def extract(self, text):
        '''Return a list of noun phrases (strings) for a body of text.

        :param str text: A string.
        '''
        parsed_sentences = self._parse_text(text)
        _extracted = []
        for s in parsed_sentences:
            tokens = s.split()
            new_np = []
            for t in tokens:
                w, tag, phrase, role = t.split('/')
                # exclude some parser errors (e.g. VB within NP),
                # extend startswith tuple if necessary
                if 'NP' in phrase and not self._is_verb(w):
                    if len(new_np) > 0 and w.lower() in START_NEW_NP:
                        _extracted.append(" ".join(new_np))
                        new_np = [w]
                    else:
                        # normalize capitalisation of sentence starters, except
                        # for nouns
                        new_np.append(w.lower() if tokens[0].startswith(w) and
                                      not tag.startswith('N') else w)
                else:
                    if len(new_np) > 0:
                        _extracted.append(" ".join(new_np))
                    new_np = []

        return self._filter_extracted(_extracted)

    def _filter_extracted(self, extracted_list):
        """Filter insignificant words for key noun phrase extraction.

        determiners, relative pronouns, reflexive pronouns
        In general, pronouns are not useful, as you need context to know what they refer to.
        Most of the pronouns, however, are filtered out by blob.noun_phrase method's
        np length (>1) filter

        :param list extracted_list: A list of noun phrases extracted from parser output.

        """
        _filtered = []
        for np in extracted_list:
            _np = np.split()
            if _np[0] in INSIGNIFICANT:
                _np.pop(0)
            try:
                if _np[-1] in INSIGNIFICANT:
                    _np.pop(-1)
                # e.g. 'welcher die ...'
                if _np[0] in INSIGNIFICANT:
                    _np.pop(0)
            except IndexError:
                _np = []
            if len(_np) > 0:
                _filtered.append(" ".join(_np))
        return _filtered

    def _parse_text(self, text):
        """Parse text (string) and return list of parsed sentences (strings).

        Each sentence consists of space separated token elements and the
        token format returned by the PatternParser is WORD/TAG/PHRASE/ROLE/(LEMMA)
        (separated by a forward slash '/')

        :param str text: A string.
        """
        parsed_text = pattern_parse(text, lemmata=False)
        return parsed_text.split('\n')

    def _is_verb(self, word_form):
        infinitive = self.verb_morphology.find_lemma(word_form)
        if infinitive in verbs:
            return True
        else:
            if self._is_in_verb_lexicon(word_form):
                return True
            else:
                return False

    def _is_in_verb_lexicon(self, word_form):
        try:
            verb_lexicon = getattr(_get_verb_lexicon, "cached")
        except AttributeError:
            verb_lexicon = _get_verb_lexicon()
        if word_form in verb_lexicon[word_form[0].lower()]:
            return True
        else:
            return False

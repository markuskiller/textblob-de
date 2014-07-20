# -*- coding: utf-8 -*-
'''Various noun phrase extractor implementations.
'''
from __future__ import absolute_import

from itertools import chain

from textblob.base import BaseNPExtractor
from textblob_de.tokenizers import get_arg_tokenizer
from textblob_de.de import parse as pattern_parse
from textblob_de.inflect import Verbs, verbs

INSIGNIFICANT = ['der', 'die', 'das', 'des', 'dem', 'ein', 'eine', 'einer', 'eines', 
                 'welcher', 'welche', 'welches']

START_NEW_NP = ['der', 'des']

class PatternParserNPExtractor(BaseNPExtractor):
    """Extract noun phrases (NP) from PatternParser() output."""
    def __init__(self):
        self.verb_lexicon = Verbs()
    
    def extract(self, text):
        '''Return a list of noun phrases (strings) for a body of text.''' 
        parsed_sentences = self._parse_text(text)
        _extracted = []
        for s in parsed_sentences:
            tokens = s.split()
            new_np = []
            for t in tokens:
                w, tag, phrase, role, lemma = t.split('/')
                # exclude some parser errors (e.g. VB within NP), 
                # extend startswith tuple if necessary
                if 'NP' in phrase and not self._is_verb(w):
                    if len(new_np) > 3 and w.lower() in START_NEW_NP:
                        _extracted.append(" ".join(new_np))
                        new_np = [w]
                    else:
                        # normalize capitalisation, except for nouns
                        new_np.append(w.lower() if not tag.startswith('N') else w)
                else:
                    if len(new_np) > 0:
                        _extracted.append(" ".join(new_np))
                    new_np = []
            
        return self._filter_extracted(_extracted)
    
    
    def _filter_extracted(self, extracted_list):
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
        token format returned by the PatternParser is WORD/TAG/PHRASE/ROLE/LEMMA
        (separated by a forward slash '/')
        """
        parsed_text = pattern_parse(text, get_arg_tokenizer(), lemmata=True)
        return parsed_text.split('\n')
    
    def _is_verb(self, word_form):
        infinitive = self.verb_lexicon.find_lemma(word_form)
        if infinitive in verbs:
            return True
        else:
            return False
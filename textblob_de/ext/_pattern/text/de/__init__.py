#### PATTERN | DE ##################################################################################
# -*- coding: utf-8 -*-
# Copyright (c) 2012 University of Antwerp, Belgium
# Author: Tom De Smedt <tom@organisms.be>
# License: BSD (see LICENSE.txt for details).
# http://www.clips.ua.ac.be/pages/pattern

# Source: https://github.com/clips/pattern/pattern/text/de/__init__.py
# git-commit: 2014-05-10 (eb98cd7)

# Modified: 2014-08-04 Markus Killer <m.killer@langui.ch>

####################################################################################################
# German linguistical tools using fast regular expressions.
from __future__ import absolute_import
import os
import sys

try:
    MODULE = os.path.dirname(os.path.realpath(__file__))
except:
    MODULE = ""

sys.path.insert(0, os.path.join(MODULE, "..", "..", "..", ".."))

from _pattern.compat import text_type, string_types, basestring, imap, unicode

# Import parser base classes.
from _pattern.text import (
    Lexicon, Model, Morphology, Context, Parser as _Parser, ngrams, pprint, commandline,
    PUNCTUATION
)
# Import parser universal tagset.
from _pattern.text import (
    penntreebank2universal,
    PTB, PENN, UNIVERSAL,
    NOUN, VERB, ADJ, ADV, PRON, DET, PREP, ADP, NUM, CONJ, INTJ, PRT, PUNC, X
)
# Import parse tree base classes.
from _pattern.text.tree import (
    Tree, Text, Sentence, Slice, Chunk, PNPChunk, Chink, Word, table,
    SLASH, WORD, POS, CHUNK, PNP, REL, ANCHOR, LEMMA, AND, OR
)
# Import sentiment analysis base classes.
from _pattern.text import (
    Sentiment, NOUN, VERB, ADJECTIVE, ADVERB
)
# Import verb tenses.
from _pattern.text import (
    INFINITIVE, PRESENT, PAST, FUTURE,
    FIRST, SECOND, THIRD,
    SINGULAR, PLURAL, SG, PL,
    INDICATIVE, IMPERATIVE, SUBJUNCTIVE,
    PROGRESSIVE,
    PARTICIPLE, GERUND
)
# Import inflection functions.
from _pattern.text.de.inflect import (
    article, referenced, DEFINITE, INDEFINITE,
    pluralize, singularize, NOUN, VERB, ADJECTIVE,
    grade, comparative, superlative, COMPARATIVE, SUPERLATIVE,
    verbs, conjugate, lemma, lexeme, tenses,
    predicative, attributive,
    gender, MASCULINE, MALE, FEMININE, FEMALE, NEUTER, NEUTRAL, PLURAL, M, F, N, PL,
            NOMINATIVE, ACCUSATIVE, DATIVE, GENITIVE, SUBJECT, OBJECT, INDIRECT, PROPERTY
)
# Import all submodules.
from _pattern.text.de import inflect

sys.path.pop(0)

#--- GERMAN PARSER ---------------------------------------------------------------------------------
# The German parser (accuracy 96% for known words) is based on Schneider & Volk's language model:
# Schneider, G. & Volk, M. (1998). 
# Adding Manual Constraints and Lexical Look-up to a Brill-Tagger for German.
# Proceedings of the ESSLLI workshop on recent advances in corpus annotation. Saarbrucken, Germany.
# http://www.zora.uzh.ch/28579/

# The lexicon uses the Stuttgart/Tubinger Tagset (STTS):
# https://files.ifi.uzh.ch/cl/tagger/UIS-STTS-Diffs.html
STTS = "stts"
stts = tagset = {
      "ADJ": "JJ",
     "ADJA": "JJ",   # das große Haus
     "ADJD": "JJ",   # er ist schnell
      "ADV": "RB",   # schon
     "APPR": "IN",   # in der Stadt
  "APPRART": "IN",   # im Haus
     "APPO": "IN",   # der Sache wegen
     "APZR": "IN",   # von jetzt an
      "ART": "DT",   # der, die, eine
   "ARTDEF": "DT",   # der, die
   "ARTIND": "DT",   # eine
     "CARD": "CD",   # zwei
  "CARDNUM": "CD",   # 3
     "KOUI": "IN",   # [um] zu leben
     "KOUS": "IN",   # weil, damit, ob
      "KON": "CC",   # und, oder, aber
    "KOKOM": "IN",   # als, wie
     "KONS": "IN",   # usw.
       "NN": "NN",   # Tisch, Herr
      "NNS": "NNS",  # Tischen, Herren
       "NE": "NNP",  # Hans, Hamburg
      "PDS": "DT",   # dieser, jener
     "PDAT": "DT",   # jener Mensch
      "PIS": "DT",   # keiner, viele, niemand
     "PIAT": "DT",   # kein Mensch
    "PIDAT": "DT",   # die beiden Brüder
     "PPER": "PRP",  # ich, er, ihm, mich, dir
     "PPOS": "PRP$", # meins, deiner
   "PPOSAT": "PRP$", # mein Buch, deine Mutter
    "PRELS": "WDT",  # der Hund, [der] bellt
   "PRELAT": "WDT",  # der Mann, [dessen] Hund bellt
      "PRF": "PRP",  # erinnere [dich]
      "PWS": "WP",   # wer
     "PWAT": "WP",   # wessen, welche
     "PWAV": "WRB",  # warum, wo, wann
      "PAV": "RB",   # dafur, dabei, deswegen, trotzdem
    "PTKZU": "TO",   # zu gehen, zu sein
   "PTKNEG": "RB",   # nicht
    "PTKVZ": "RP",   # pass [auf]!
   "PTKANT": "UH",   # ja, nein, danke, bitte
     "PTKA": "RB",   # am schönsten, zu schnell 
    "VVFIN": "VB",   # du [gehst], wir [kommen] an
    "VAFIN": "VB",   # du [bist], wir [werden]
    "VVINF": "VB",   # gehen, ankommen
    "VAINF": "VB",   # werden, sein
    "VVIZU": "VB",   # anzukommen
    "VVIMP": "VB",   # [komm]!
    "VAIMP": "VB",   # [sei] ruhig!
     "VVPP": "VBN",  # gegangen, angekommen
     "VAPP": "VBN",  # gewesen
    "VMFIN": "MD",   # dürfen
    "VMINF": "MD",   # wollen
     "VMPP": "MD",   # gekonnt
     "SGML": "SYM",  #
       "FM": "FW",   #
      "ITJ": "UH",   # ach, tja
       "XY": "NN",   #
       "XX": "NN",   #
    "LINUM": "LS",   # 1.
        "C": ",",    # ,
       "Co": ":",    # :
       "Ex": ".",    # ! 
       "Pc": ")",    # )
       "Po": "(",    # (
        "Q": ".",    # ?
      "QMc": "\"",   # "
      "QMo": "\"",   # "
        "S": ".",    # .
       "Se": ":",    # ;
}

def stts2penntreebank(token, tag):
    """ Converts an STTS tag to a Penn Treebank II tag.
        For example: ohne/APPR => ohne/IN
    """
    return (token, stts.get(tag, tag))
    
def stts2universal(token, tag):
    """ Converts an STTS tag to a universal tag.
        For example: ohne/APPR => ohne/PREP
    """
    if tag in ("KON", "KOUI", "KOUS", "KOKOM"):
        return (token, CONJ)
    if tag in ("PTKZU", "PTKNEG", "PTKVZ", "PTKANT"):
        return (token, PRT)
    if tag in ("PDF", "PDAT", "PIS", "PIAT", "PIDAT", "PPER", "PPOS", "PPOSAT"): 
        return (token, PRON)
    if tag in ("PRELS", "PRELAT", "PRF", "PWS", "PWAT", "PWAV", "PAV"):
        return (token, PRON)
    return penntreebank2universal(*stts2penntreebank(token, tag))

#let's add some legal abbreviations, too
#let's also completely rule out at least simple ordinals
#let's also rule out anything that could be a date
ABBREVIATIONS = set((
    "Abs.", "Abt.", "Ass.", "Br.", "Ch.", "Chr.", "Cie.", "Co.", "Dept.", "Diff.", 
    "Dr.", "Eidg.", "Exp.", "Fam.", "Fr.", "Hrsg.", "Inc.", "Inv.", "Jh.", "Jt.", "Kt.", 
    "Mio.", "Mrd.", "Mt.", "Mte.", "Nr.", "Nrn.", "Ord.", "Ph.", "Phil.", "Pkt.", 
    "Prof.", "Pt.", " S.", "St.", "Stv.", "Tit.", "VII.", "al.", "begr.","bzw.", 
    "chem.", "dent.", "dipl.", "e.g.", "ehem.", "etc.", "excl.", "exkl.", "gem.", "hum.", 
    "i.e.", "incl.", "ing.", "inkl.", "int.", "iur.", "lic.", "med.", "no.", "oec.", 
    "phil.", "phys.", "pp.", "psych.", "publ.", "rer.", "sc.", "soz.", "spez.", "stud.", 
    "theol.", "usw.", "v.", "vet.", "vgl.", "vol.", "wiss.",
    "d.h.", "h.c.", u"o.ä.", "u.a.", "z.B.", "z.T.", "z.Zt.", "z. B.", "d. h.", "h. c.", 
    u"o. ä.", "u. a.", "z. B.", "z. T.", "z. Zt.",
    "BGBl.", "ABl.", "Bundesgesetzbl.",
    "0.", "1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.",
    "0 .", "1 .", "2 .", "3 .", "4 .", "5 .", "6 .", "7 .", "8 .", "9 .",
    "1. Januar", "2. Januar", "3. Januar", "4. Januar", "5. Januar", "6. Januar", 
    "7. Januar", "8. Januar", "9. Januar", "10. Januar", "11. Januar", "12. Januar", 
    "13. Januar", "14. Januar", "15. Januar", "16. Januar", "17. Januar", "18. Januar", 
    "19. Januar", "20. Januar", "21. Januar", "22. Januar", "23. Januar", "24. Januar", 
    "25. Januar", "26. Januar", "27. Januar", "28. Januar", "29. Januar", "30. Januar", 
    "31. Januar", "1. Februar", "2. Februar", "3. Februar", "4. Februar", "5. Februar", 
    "6. Februar", "7. Februar", "8. Februar", "9. Februar", "10. Februar", "11. Februar", 
    "12. Februar", "13. Februar", "14. Februar", "15. Februar", "16. Februar", "17. Februar", 
    "18. Februar", "19. Februar", "20. Februar", "21. Februar", "22. Februar", "23. Februar", 
    "24. Februar", "25. Februar", "26. Februar", "27. Februar", "28. Februar", "29. Februar", 
    "1. März", "2. März", "3. März", "4. März", "5. März", "6. März", "7. März", "8. März", 
    "9. März", "10. März", "11. März", "12. März", "13. März", "14. März", "15. März", "16. März", 
    "17. März", "18. März", "19. März", "20. März", "21. März", "22. März", "23. März", "24. März", 
    "25. März", "26. März", "27. März", "28. März", "29. März", "30. März", "31. März", "1. April", 
    "2. April", "3. April", "4. April", "5. April", "6. April", "7. April", "8. April", "9. April", 
    "10. April", "11. April", "12. April", "13. April", "14. April", "15. April", "16. April", 
    "17. April", "18. April", "19. April", "20. April", "21. April", "22. April", "23. April", 
    "24. April", "25. April", "26. April", "27. April", "28. April", "29. April", "30. April", 
    "1. Mai", "2. Mai", "3. Mai", "4. Mai", "5. Mai", "6. Mai", "7. Mai", "8. Mai", "9. Mai", 
    "10. Mai", "11. Mai", "12. Mai", "13. Mai", "14. Mai", "15. Mai", "16. Mai", "17. Mai", 
    "18. Mai", "19. Mai", "20. Mai", "21. Mai", "22. Mai", "23. Mai", "24. Mai", "25. Mai", 
    "26. Mai", "27. Mai", "28. Mai", "29. Mai", "30. Mai", "31. Mai", "1. Juni", "2. Juni", 
    "3. Juni", "4. Juni", "5. Juni", "6. Juni", "7. Juni", "8. Juni", "9. Juni", "10. Juni", 
    "11. Juni", "12. Juni", "13. Juni", "14. Juni", "15. Juni", "16. Juni", "17. Juni", 
    "18. Juni", "19. Juni", "20. Juni", "21. Juni", "22. Juni", "23. Juni", "24. Juni", 
    "25. Juni", "26. Juni", "27. Juni", "28. Juni", "29. Juni", "30. Juni", "1. Juli", 
    "2. Juli", "3. Juli", "4. Juli", "5. Juli", "6. Juli", "7. Juli", "8. Juli", "9. Juli", 
    "10. Juli", "11. Juli", "12. Juli", "13. Juli", "14. Juli", "15. Juli", "16. Juli", 
    "17. Juli", "18. Juli", "19. Juli", "20. Juli", "21. Juli", "22. Juli", "23. Juli", 
    "24. Juli", "25. Juli", "26. Juli", "27. Juli", "28. Juli", "29. Juli", "30. Juli", 
    "31. Juli", "1. August", "2. August", "3. August", "4. August", "5. August", "6. August", 
    "7. August", "8. August", "9. August", "10. August", "11. August", "12. August", "13. August", 
    "14. August", "15. August", "16. August", "17. August", "18. August", "19. August", "20. August", 
    "21. August", "22. August", "23. August", "24. August", "25. August", "26. August", "27. August", 
    "28. August", "29. August", "30. August", "31. August", "1. September", "2. September", "3. September", 
    "4. September", "5. September", "6. September", "7. September", "8. September", "9. September", 
    "10. September", "11. September", "12. September", "13. September", "14. September", "15. September", 
    "16. September", "17. September", "18. September", "19. September", "20. September", "21. September", 
    "22. September", "23. September", "24. September", "25. September", "26. September", "27. September", 
    "28. September", "29. September", "30. September", "1. Oktober", "2. Oktober", 
    "3. Oktober", "4. Oktober", "5. Oktober", "6. Oktober", "7. Oktober", "8. Oktober", "9. Oktober", 
    "10. Oktober", "11. Oktober", "12. Oktober", "13. Oktober", "14. Oktober", "15. Oktober", "16. Oktober", 
    "17. Oktober", "18. Oktober", "19. Oktober", "20. Oktober", "21. Oktober", "22. Oktober", "23. Oktober", 
    "24. Oktober", "25. Oktober", "26. Oktober", "27. Oktober", "28. Oktober", "29. Oktober", "30. Oktober", 
    "31. Oktober", "1. November", "2. November", "3. November", "4. November", "5. November", 
    "6. November", "7. November", "8. November", "9. November", "10. November", "11. November", 
    "12. November", "13. November", "14. November", "15. November", "16. November", "17. November", 
    "18. November", "19. November", "20. November", "21. November", "22. November", "23. November", 
    "24. November", "25. November", "26. November", "27. November", "28. November", "29. November", 
    "30. November", "1. Dezember", "2. Dezember", "3. Dezember", "4. Dezember", "5. Dezember", "6. Dezember", 
    "7. Dezember", "8. Dezember", "9. Dezember", "10. Dezember", "11. Dezember", "12. Dezember", "13. Dezember", 
    "14. Dezember", "15. Dezember", "16. Dezember", "17. Dezember", "18. Dezember", "19. Dezember", "20. Dezember", 
    "21. Dezember", "22. Dezember", "23. Dezember", "24. Dezember", "25. Dezember", "26. Dezember", "27. Dezember", 
    "28. Dezember", "29. Dezember", "30. Dezember", "31. Dezember", "1. 1.", "2. 1.", "3. 1.", "4. 1.", "5. 1.", 
    "6. 1.", "7. 1.", "8. 1.", "9. 1.", "10. 1.", "11. 1.", "12. 1.", "13. 1.", "14. 1.", "15. 1.", "16. 1.", 
    "17. 1.", "18. 1.", "19. 1.", "20. 1.", "21. 1.", "22. 1.", "23. 1.", "24. 1.", "25. 1.", "26. 1.", "27. 1.", 
    "28. 1.", "29. 1.", "30. 1.", "31. 1.", "1. 2.", "2. 2.", "3. 2.", "4. 2.", "5. 2.", "6. 2.", "7. 2.", "8. 2.", 
    "9. 2.", "10. 2.", "11. 2.", "12. 2.", "13. 2.", "14. 2.", "15. 2.", "16. 2.", "17. 2.", "18. 2.", "19. 2.", 
    "20. 2.", "21. 2.", "22. 2.", "23. 2.", "24. 2.", "25. 2.", "26. 2.", "27. 2.", "28. 2.", "29. 2.", 
    "1. 3.", "2. 3.", "3. 3.", "4. 3.", "5. 3.", "6. 3.", "7. 3.", "8. 3.", "9. 3.", "10. 3.", "11. 3.", "12. 3.", 
    "13. 3.", "14. 3.", "15. 3.", "16. 3.", "17. 3.", "18. 3.", "19. 3.", "20. 3.", "21. 3.", "22. 3.", "23. 3.", 
    "24. 3.", "25. 3.", "26. 3.", "27. 3.", "28. 3.", "29. 3.", "30. 3.", "31. 3.", "1. 4.", "2. 4.", "3. 4.", 
    "4. 4.", "5. 4.", "6. 4.", "7. 4.", "8. 4.", "9. 4.", "10. 4.", "11. 4.", "12. 4.", "13. 4.", "14. 4.", 
    "15. 4.", "16. 4.", "17. 4.", "18. 4.", "19. 4.", "20. 4.", "21. 4.", "22. 4.", "23. 4.", "24. 4.", 
    "25. 4.", "26. 4.", "27. 4.", "28. 4.", "29. 4.", "30. 4.", "1. 5.", "2. 5.", "3. 5.", "4. 5.", "5. 5.", 
    "6. 5.", "7. 5.", "8. 5.", "9. 5.", "10. 5.", "11. 5.", "12. 5.", "13. 5.", "14. 5.", "15. 5.", "16. 5.", 
    "17. 5.", "18. 5.", "19. 5.", "20. 5.", "21. 5.", "22. 5.", "23. 5.", "24. 5.", "25. 5.", "26. 5.", "27. 5.", 
    "28. 5.", "29. 5.", "30. 5.", "31. 5.", "1. 6.", "2. 6.", "3. 6.", "4. 6.", "5. 6.", "6. 6.", "7. 6.", "8. 6.", 
    "9. 6.", "10. 6.", "11. 6.", "12. 6.", "13. 6.", "14. 6.", "15. 6.", "16. 6.", "17. 6.", "18. 6.", "19. 6.", 
    "20. 6.", "21. 6.", "22. 6.", "23. 6.", "24. 6.", "25. 6.", "26. 6.", "27. 6.", "28. 6.", "29. 6.", "30. 6.", 
    "1. 7.", "2. 7.", "3. 7.", "4. 7.", "5. 7.", "6. 7.", "7. 7.", "8. 7.", "9. 7.", "10. 7.", "11. 7.", "12. 7.", 
    "13. 7.", "14. 7.", "15. 7.", "16. 7.", "17. 7.", "18. 7.", "19. 7.", "20. 7.", "21. 7.", "22. 7.", "23. 7.", 
    "24. 7.", "25. 7.", "26. 7.", "27. 7.", "28. 7.", "29. 7.", "30. 7.", "31. 7.", "1. 8.", "2. 8.", "3. 8.", 
    "4. 8.", "5. 8.", "6. 8.", "7. 8.", "8. 8.", "9. 8.", "10. 8.", "11. 8.", "12. 8.", "13. 8.", "14. 8.", 
    "15. 8.", "16. 8.", "17. 8.", "18. 8.", "19. 8.", "20. 8.", "21. 8.", "22. 8.", "23. 8.", "24. 8.", "25. 8.", 
    "26. 8.", "27. 8.", "28. 8.", "29. 8.", "30. 8.", "31. 8.", "1. 9.", "2. 9.", "3. 9.", "4. 9.", "5. 9.", 
    "6. 9.", "7. 9.", "8. 9.", "9. 9.", "10. 9.", "11. 9.", "12. 9.", "13. 9.", "14. 9.", "15. 9.", "16. 9.", 
    "17. 9.", "18. 9.", "19. 9.", "20. 9.", "21. 9.", "22. 9.", "23. 9.", "24. 9.", "25. 9.", "26. 9.", 
    "27. 9.", "28. 9.", "29. 9.", "30. 9.", "1. 10.", "2. 10.", "3. 10.", "4. 10.", "5. 10.", "6. 10.", 
    "7. 10.", "8. 10.", "9. 10.", "10. 10.", "11. 10.", "12. 10.", "13. 10.", "14. 10.", "15. 10.", "16. 10.", 
    "17. 10.", "18. 10.", "19. 10.", "20. 10.", "21. 10.", "22. 10.", "23. 10.", "24. 10.", "25. 10.", 
    "26. 10.", "27. 10.", "28. 10.", "29. 10.", "30. 10.", "31. 10.", "1. 11.", "2. 11.", "3. 11.", 
    "4. 11.", "5. 11.", "6. 11.", "7. 11.", "8. 11.", "9. 11.", "10. 11.", "11. 11.", "12. 11.", "13. 11.", 
    "14. 11.", "15. 11.", "16. 11.", "17. 11.", "18. 11.", "19. 11.", "20. 11.", "21. 11.", "22. 11.", 
    "23. 11.", "24. 11.", "25. 11.", "26. 11.", "27. 11.", "28. 11.", "29. 11.", "30. 11.", "1. 12.", 
    "2. 12.", "3. 12.", "4. 12.", "5. 12.", "6. 12.", "7. 12.", "8. 12.", "9. 12.", "10. 12.", "11. 12.", 
    "12. 12.", "13. 12.", "14. 12.", "15. 12.", "16. 12.", "17. 12.", "18. 12.", "19. 12.", "20. 12.", 
    "21. 12.", "22. 12.", "23. 12.", "24. 12.", "25. 12.", "26. 12.", "27. 12.", "28. 12.", "29. 12.", 
    "30. 12.", "31. 12.", "
))

def find_lemmata(tokens):
    """ Annotates the tokens with lemmata for plural nouns and conjugated verbs,
        where each token is a [word, part-of-speech] list.
    """
    for token in tokens:
        word, pos, lemma = token[0], token[1], token[0]
        if pos.startswith(("DT", "JJ")):
            lemma = predicative(word)  
        if pos == "NNS":
            lemma = singularize(word)
        if pos.startswith(("VB", "MD")):
            lemma = conjugate(word, INFINITIVE) or word
        token.append(lemma.lower())
    return tokens
    
class Parser(_Parser):
    
    def find_tokens(self, tokens, **kwargs):
        kwargs.setdefault("abbreviations", ABBREVIATIONS)
        kwargs.setdefault("replace", {})
        return _Parser.find_tokens(self, tokens, **kwargs)
        
    def find_lemmata(self, tokens, **kwargs):
        return find_lemmata(tokens)
        
    def find_tags(self, tokens, **kwargs):
        if kwargs.get("tagset") in (PENN, None):
            kwargs.setdefault("map", lambda token, tag: stts2penntreebank(token, tag))
        if kwargs.get("tagset") == UNIVERSAL:
            kwargs.setdefault("map", lambda token, tag: stts2universal(token, tag))
        if kwargs.get("tagset") is STTS:
            kwargs.setdefault("map", lambda token,tag: (token, tag))
        # The lexicon uses Swiss spelling: "ss" instead of "ß".
        # We restore the "ß" after parsing.
        tokens_ss = [t.replace(u"ß", "ss") for t in tokens]
        tokens_ss = _Parser.find_tags(self, tokens_ss, **kwargs)
        return [[w] + tokens_ss[i][1:] for i, w in enumerate(tokens)]

parser = Parser(
     lexicon = os.path.join(MODULE, "de-lexicon.txt"),
   frequency = os.path.join(MODULE, "de-frequency.txt"),
  morphology = os.path.join(MODULE, "de-morphology.txt"),
     context = os.path.join(MODULE, "de-context.txt"),
     default = ("NN", "NE", "CARDNUM"),
    language = "de"
)

lexicon = parser.lexicon # Expose lexicon.

def tokenize(s, *args, **kwargs):
    """ Returns a list of sentences, where punctuation marks have been split from words.
    """
    return parser.find_tokens(s, *args, **kwargs)

def parse(s, *args, **kwargs):
    """ Returns a tagged Unicode string.
    """
    return parser.parse(s, *args, **kwargs)

def parsetree(s, *args, **kwargs):
    """ Returns a parsed Text from the given string.
    """
    return Text(parse(s, *args, **kwargs))

def tree(s, token=[WORD, POS, CHUNK, PNP, REL, LEMMA]):
    """ Returns a parsed Text from the given parsed string.
    """
    return Text(s, token)
    
def tag(s, tokenize=True, encoding="utf-8", **kwargs):
    """ Returns a list of (token, tag)-tuples from the given string.
    """
    tags = []
    for sentence in parse(s, tokenize, True, False, False, False, encoding, **kwargs).split():
        for token in sentence:
            tags.append((token[0], token[1]))
    return tags
    
def keywords(s, top=10, **kwargs):
    """ Returns a sorted list of keywords in the given string.
    """
    return parser.find_keywords(s, top=top, frequency=parser.frequency)

split = tree # Backwards compatibility.

#---------------------------------------------------------------------------------------------------
# python -m pattern.de xml -s "Ein Unglück kommt selten allein." -OTCL

if __name__ == "__main__":
    commandline(parse)

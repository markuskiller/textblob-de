# -*- coding: utf-8 -*-
'''Code adapted from the ``pattern.de`` library.

:repo: `https://github.com/clips/pattern`_
:source: pattern/text/de/__init__.py
:version: 2014-05-10 (eb98cd722e)

:modified: July 2014 <m.killer@langui.ch>

See the NOTICE file for license information.
'''

#### PATTERN | DE ########################################################
# -*- coding: utf-8 -*-
# Copyright (c) 2012 University of Antwerp, Belgium
# Author: Tom De Smedt <tom@organisms.be>
# License: BSD (see LICENSE.txt for details).
# http://www.clips.ua.ac.be/pages/pattern

##########################################################################
# German linguistical tools using fast regular expressions.
from __future__ import absolute_import
import os
import sys

try:
    MODULE = os.path.dirname(os.path.realpath(__file__))
except:
    MODULE = ""

sys.path.insert(0, os.path.join(MODULE, "..", "..", "..", ".."))

from textblob_de.compat import text_type, string_types, basestring, imap, unicode

# Import parser base classes.
from textblob_de._text import (
    Lexicon, Model, Morphology, Context, Parser as _Parser, ngrams, pprint, commandline,
    PUNCTUATION, ABBREVIATIONS_DE
)
# Import parser universal tagset.
from textblob_de._text import (
    penntreebank2universal,
    PTB, PENN, UNIVERSAL,
    NOUN, VERB, ADJ, ADV, PRON, DET, PREP, ADP, NUM, CONJ, INTJ, PRT, PUNC, X
)
# Import parse tree base classes.
from textblob_de._tree import (
    Tree, Text, Sentence, Slice, Chunk, PNPChunk, Chink, Word, table,
    SLASH, WORD, POS, CHUNK, PNP, REL, ANCHOR, LEMMA, AND, OR
)
# Import sentiment analysis base classes.
from textblob_de._text import (
    Sentiment as _Sentiment,
    NOUN, VERB, ADJECTIVE, ADVERB
)
# Import verb tenses.
from textblob_de._text import (
    INFINITIVE, PRESENT, PAST, FUTURE,
    FIRST, SECOND, THIRD,
    SINGULAR, PLURAL, SG, PL,
    INDICATIVE, IMPERATIVE, SUBJUNCTIVE,
    PROGRESSIVE,
    PARTICIPLE, GERUND
)
# Import inflection functions.
from textblob_de.inflect import (
    article, referenced, DEFINITE, INDEFINITE,
    pluralize, singularize, NOUN, VERB, ADJECTIVE,
    grade, comparative, superlative, COMPARATIVE, SUPERLATIVE,
    verbs, conjugate, lemma, lexeme, tenses,
    predicative, attributive,
    gender, MASCULINE, MALE, FEMININE, FEMALE, NEUTER, NEUTRAL, PLURAL, M, F, N, PL,
    NOMINATIVE, ACCUSATIVE, DATIVE, GENITIVE, SUBJECT, OBJECT, INDIRECT, PROPERTY
)
# Import all submodules.
from textblob_de import inflect

sys.path.pop(0)

#--- GERMAN PARSER -------------------------------------------------------
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
    "PPOS": "PRP$",  # meins, deiner
    "PPOSAT": "PRP$",  # mein Buch, deine Mutter
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
    if tag in (
            "PDF", "PDAT", "PIS", "PIAT", "PIDAT", "PPER", "PPOS", "PPOSAT"):
        return (token, PRON)
    if tag in ("PRELS", "PRELAT", "PRF", "PWS", "PWAT", "PWAV", "PAV"):
        return (token, PRON)
    return penntreebank2universal(*stts2penntreebank(token, tag))


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

    def find_tokens(self, tokens, tokenizer, **kwargs):
        kwargs.setdefault("abbreviations", ABBREVIATIONS_DE)
        kwargs.setdefault("replace", {})
        # return _Parser.find_tokens(self, tokens, **kwargs)
        return tokenizer.sent_tokenize(tokens, **kwargs)

    def find_lemmata(self, tokens, **kwargs):
        return find_lemmata(tokens)

    def find_tags(self, tokens, **kwargs):
        if kwargs.get("tagset") in (PENN, None):
            kwargs.setdefault(
                "map",
                lambda token,
                tag: stts2penntreebank(
                    token,
                    tag))
        if kwargs.get("tagset") == UNIVERSAL:
            kwargs.setdefault(
                "map",
                lambda token,
                tag: stts2universal(
                    token,
                    tag))
        if kwargs.get("tagset") is STTS:
            kwargs.setdefault("map", lambda token, tag: (token, tag))
        # The lexicon uses Swiss spelling: "ss" instead of "ß".
        # We restore the "ß" after parsing.
        tokens_ss = [t.replace(u"ß", "ss") for t in tokens]
        tokens_ss = _Parser.find_tags(self, tokens_ss, **kwargs)
        return [[w] + tokens_ss[i][1:] for i, w in enumerate(tokens)]

parser = Parser(
    lexicon=os.path.join(MODULE, "de-lexicon.txt"),
    frequency=os.path.join(MODULE, "de-frequency.txt"),
    morphology=os.path.join(MODULE, "de-morphology.txt"),
    context=os.path.join(MODULE, "de-context.txt"),
    default=("NN", "NE", "CARDNUM"),
    language = "de"
)

lexicon = parser.lexicon  # Expose lexicon.


def tokenize(s, *args, **kwargs):
    """ Returns a list of sentences, where punctuation marks have been split from words.
    """
    return parser.find_tokens(s, *args, **kwargs)


def parse(s, tokenizer, *args, **kwargs):
    """ Returns a tagged Unicode string.
    """
    return parser.parse(s, tokenizer, *args, **kwargs)


def parsetree(s, *args, **kwargs):
    """ Returns a parsed Text from the given string.
    """
    return Text(parse(s, *args, **kwargs))


def tree(s, token=[WORD, POS, CHUNK, PNP, REL, LEMMA]):
    """ Returns a parsed Text from the given parsed string.
    """
    return Text(s, token)


def tag(s, tokenizer, tokenize=True, encoding="utf-8", **kwargs):
    """ Returns a list of (token, tag)-tuples from the given string.
    """
    tags = []
    for sentence in parse(s, tokenizer, tokenize, True, False, False, False, encoding, **kwargs).split():
        for token in sentence:
            tags.append((token[0], token[1]))
    return tags


def keywords(s, top=10, **kwargs):
    """ Returns a sorted list of keywords in the given string.
    """
    return parser.find_keywords(s, top=top, frequency=parser.frequency)

split = tree  # Backwards compatibility.


#################### SENTIMENT DETECTION ##################################
# copied from 'textblob_fr.fr.py', needs to be adapted when
class Sentiment(_Sentiment):

    def load(self, path=None):
        _Sentiment.load(self, path)
        # Map "précaire" to "precaire" (without diacritics, +1% accuracy).
        if not path:
            for w, pos in list(self.items()):
                w0 = w
                if not w.endswith((u"à", u"è", u"é", u"ê", u"ï")):
                    w = w.replace(u"à", "a")
                    w = w.replace(u"é", "e")
                    w = w.replace(u"è", "e")
                    w = w.replace(u"ê", "e")
                    w = w.replace(u"ï", "i")
                if w != w0:
                    for pos, (p, s, i) in pos.items():
                        self.annotate(w, pos, p, s, i)


def sentiment(text, _tokenizer):
    s = Sentiment(
        path=os.path.join(MODULE, "de-sentiment.xml"),
        synset=None,
        negations=(
            "nicht",
            "ohne",
            "nie",
            "nein",
            "kein",
            "keiner",
            "keine",
            "nichts"),
        modifiers = ("RB", "JJ"),
        modifier = lambda w: w.endswith("lich"),
        tokenizer = _tokenizer,
        language = "de"
    )
    return s(text)


def polarity(s, **kwargs):
    """ Returns the sentence polarity (positive/negative) between -1.0 and 1.0.
    """
    return sentiment(s, **kwargs)[0]


def subjectivity(s, **kwargs):
    """ Returns the sentence subjectivity (objective/subjective) between 0.0 and 1.0.
    """
    return sentiment(s, **kwargs)[1]


def positive(s, threshold=0.1, **kwargs):
    """ Returns True if the given sentence has a positive sentiment (polarity >= threshold).
    """
    return polarity(s, **kwargs) >= threshold

#################### END SENTIMENT DETECTION ##################################

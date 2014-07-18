# -*- coding: utf-8 -*-
'''Code adapted from ``textblob`` main package.

:repo: `https://github.com/sloria/TextBlob`_
:source: textblob/blob.py
:version: 2013-10-21 (a88e86a76a)

:modified: July 2014 <m.killer@langui.ch>

'''
from __future__ import absolute_import

from textblob import TextBlob, Sentence, WordList, Word
from textblob.decorators import cached_property
from textblob.utils import PUNCTUATION_REGEX

from textblob_de.compat import unicode
from textblob_de.tokenizers import get_arg_tokenizer, NLTKPunktTokenizer, PatternTokenizer
from textblob_de.taggers import PatternTagger
from textblob_de.parsers import get_kwarg_lemmata, PatternParser
from textblob_de.sentiments import PatternAnalyzer


class TextBlobDE(TextBlob):

    '''Pass German default values to TextBlob():

    :param str text: A string.
    :param tokenizer: (optional) A tokenizer instance. If ``None``, defaults to
        :class:`NLTKPunktTokenizer() <textblob_de.tokenizers.NLTKPunktTokenizer>`.
    :param np_extractor: (optional) An NPExtractor instance. If ``None``,
        defaults to :class:`FastNPExtractor() <textblob.en.np_extractors.FastNPExtractor>`.
    :param pos_tagger: (optional) A Tagger instance. If ``None``, defaults to
        :class:`PatternTagger <textblob_de.taggers.PatternTagger>`.
    :param analyzer: (optional) A sentiment analyzer. If ``None``, defaults to
        :class:`PatternAnalyzer <textblob_de.sentiments.PatternAnalyzer>`.
    :param classifier: (optional) A classifier.
    :param parser_show_lemmata: (optional and temporary) Parser output prints lemmata (if available).

    '''

    # named keywords arguments are included for autocompletion reasons

    def __init__(self, text,
                 tokenizer=None,
                 pos_tagger=None,
                 np_extractor=None,
                 analyzer=None,
                 parser=None,
                 classifier=None,
                 clean_html=False,
                 parser_show_lemmata=False):
        '''Initialize TextBlob() with German default values.'''

        self.tokenizer = tokenizer if tokenizer else NLTKPunktTokenizer()
        self.pos_tagger = pos_tagger if pos_tagger else PatternTagger()
        self.parser = parser if parser else PatternParser()
        self.parser_show_lemmata = True if parser_show_lemmata else False
        self.analyzer = analyzer if analyzer else PatternAnalyzer()
        self.classifier = classifier if classifier else None

        from textblob.utils import lowerstrip
        self.raw = self.string = text
        self.stripped = lowerstrip(self.raw, all=True)

        #: Temporary workarounds until ``TextBlob.parse`` and ``TextBlob.tag``
        #: methods accept ``*args, **kwargs``
        #:
        #: Make tokenizer accessible for PatternParser/PatternTagger/PatternAnalyzer
        #: This will probably not work if there are mixed calls to two or more
        #: different  TextBlob instances. But it is as close as we can
        #: get to using the same tokenizer across all different tools.
        #: Possible long-term solution: add tokenizer as mandatory argument to
        #: :py:meth:`tag` and :py:meth:`parse` in :py:class:`BaseBlob`.
        setattr(get_arg_tokenizer, "tokenizer", self.tokenizer)
        if self.parser_show_lemmata:
            setattr(get_kwarg_lemmata, "lemmata", True)
        else:
            if hasattr(get_kwarg_lemmata, "lemmata"):
                delattr(get_kwarg_lemmata, "lemmata")

    @cached_property
    def words(self):
        """Return a list of word tokens. This excludes punctuation characters.
        If you want to include punctuation characters, access the ``tokens``
        property.

        :returns: A :class:`WordList <WordList>` of word tokens.
        """
        return WordList(self.tokenizer.tokenize(self.raw, include_punc=False))

    @cached_property
    def tokens(self):
        '''Return a list of tokens, using this blob's tokenizer object
        (defaults to :class:`WordTokenizer <textblob.tokenizers.WordTokenizer>`).
        '''
        return WordList(self.tokenizer.tokenize(self.raw, include_punc=True))

    def parse(self, parser=None):
        """Parse the text.

        :param parser: (optional) A parser instance. If ``None``, defaults to
            this blob's default parser.

        .. versionadded:: 0.6.0
        """
        p = parser if parser is not None else self.parser
        return p.parse(self.raw)

    def _create_sentence_objects(self):
        '''Returns a list of Sentence objects from the raw text.


        '''
        sentence_objects = []
        sentences = self.tokenizer.sent_tokenize(self.raw)
        char_index = 0  # Keeps track of character index within the blob
        for sent in sentences:
                # Compute the start and end indices of the sentence
                # within the blob. This only works if the sentence splitter
                # does not perform any character replacements or changes to
                # white space.
                # Working: NLTKPunktTokenizer
                # Not working: PatternTokenizer
            try:
                start_index = self.raw.index(sent, char_index)
                char_index += len(sent)
                end_index = start_index + len(sent)
            except ValueError:
                start_index = None
                end_index = None
            # Sentences share the same models as their parent blob
            s = Sentence(sent, start_index=start_index, end_index=end_index,
                         tokenizer=self.tokenizer, np_extractor=self.np_extractor,
                         pos_tagger=self.pos_tagger, analyzer=self.analyzer,
                         parser=self.parser, classifier=self.classifier)
            sentence_objects.append(s)
        return sentence_objects

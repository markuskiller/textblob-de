.. textblob documentation master file
   adapted from the main `TextBlob`_ library by Steven Loria

textblob-de
===========

Release |version| (:ref:`Changelog`)

`TextBlob`_ is a Python (2 and 3) library for processing textual data. 
It is being developed by `Steven Loria`_. It provides a simple API for diving into 
common natural language processing (NLP) tasks such as part-of-speech tagging, 
noun phrase extraction, sentiment analysis, classification, 
translation, and more.

**`textblob-de`** is the **German language extension** for `TextBlob`_.

.. code-block:: python

    from textblob_de import TextBlobDE

    text = '''
    "Der Blob" macht in seiner unbekümmert-naiven Weise einfach nur Spass.
    Er hat eben den gewissen Charme, bei dem auch die eher hölzerne Regie und 
    das konfuse Drehbuch nicht weiter stören.
    '''

    blob = TextBlobDE(text)
    blob.tags           # [('Der', 'DT'), ('Blob', 'NN'), ('macht', 'VB'), 
                        #  ('in', 'IN'), ('seiner', 'PRP$'), ...]

    blob.noun_phrases   # WordList(['Der Blob', 'seiner unbekümmert-naiven Weise', 
                        #           'den gewissen Charme', 'hölzerne Regie', 
                        #           'konfuse Drehbuch'])


    for sentence in blob.sentences:
        print(sentence.sentiment.polarity)
    # 1.0
    # 0.0

    blob.translate(to="es")  # '" The Blob " hace a su manera ingenua...'


For a complete overview of `TextBlob` 's features, see documentation of
the main `TextBlob`_ library.

The docs of the German language extension focus on additions/differences to
`TextBlob`_ and provide a detailed API reference.

Guide
=====

.. toctree::
   :maxdepth: 2

   readme
   quickstart
   advanced_usage
   extensions
   api_reference

Project info
============

.. toctree::
   :maxdepth: 1

   changelog
   authors
   license
   contributing
   make_info
   project_makefile
   docs_makefile


.. _TextBlob: http://textblob.readthedocs.org/
.. _Steven Loria: http://stevenloria.com/

.. _advanced:

Advanced Usage: Overriding Models and the Blobber Class
=======================================================

Follow the `Advanced Usage guide <http://textblob.readthedocs.org/en/dev/advanced_usage.html>`_ 
in the documentation of the main package (using German examples). The following 
minimal replacements are necessary in order to enable the use of the German default models:

+--------------------+-----------------+
| **Instead of:**    | **Use:**        |
+====================+=================+
| ``textblob``       | ``textblob_de`` |
+--------------------+-----------------+
| ``TextBlob``       | ``TextBlobDE``  |
+--------------------+-----------------+
| ``Blobber``        | ``BlobberDE``   |
+--------------------+-----------------+



===
OCR
===
To use: |Tools tab| |Right arrow| |OCR button|

Because OCR is an intensive operation, documents are queued for OCR for
later handling, the amount of documents processed in parallel is
controlled by the :setting:`OCR_NODE_CONCURRENT_EXECUTION` configuration
option.  Ideally the machine serving **Mayan EDMS** should disable OCR 
processing by settings this options to 0, with other machines or cloud
instances then connected to the same database doing the OCR processing.
The document is checked to see if there are text parsers available, is
no parser is available for that file type then the document is passed
to Tesseract_ page by page and the results stored per page, this is to
keep the page image in sync with the transcribed text.  However when
viewing the document in the details tab all the pages text are
concatenated and shown to the user.  All newly uploaded documents will be
queued automatically for OCR, if this is not desired setting the :setting:`OCR_AUTOMATIC_OCR`
option to ``False`` would stop this behavior.

---------------------
Document text parsers
---------------------
When checking queued documents, **Mayan EDMS** will first try to extract
text using one of the registered parsers corresponding to the document 
MIME type.  Only when failing to extract any text using a parser,
**Mayan EDMS** will fallback to process the document's image representation
using the OCR engine Tesseract_ and the OCR preprosessor unpaper_.


.. _Tesseract: http://code.google.com/p/tesseract-ocr/
.. _unpaper: http://unpaper.berlios.de/

.. |Tools tab| image:: /_static/tools_tab.png
 :alt: Tags tab
 :align: middle

.. |Right arrow| image:: /_static/arrow_right.png
 :alt: Right arrow
 :align: middle

.. |OCR button| image:: /_static/ocr_button.png
 :alt: OCR button
 :align: middle

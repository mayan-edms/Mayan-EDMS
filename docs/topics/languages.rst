=========
Languages
=========

The list of languages choices in the language dropdown used for documents is
based on the current ISO 639 list. This list can be quite extensive. To reduce
the number of languages available use the settings ``DOCUMENTS_LANGUAGE_CODES``,
and set it to a nested list of abbreviations + languages names like::

    DOCUMENTS_LANGUAGE_CODES = ('eng', 'spa')


The default language to appear on the dropdown can also be configured using::

    DOCUMENTS_LANGUAGE = 'spa'

Use the correct ISO 639-3 language abbreviation (https://en.wikipedia.org/wiki/ISO_639)
as this code is used in several subsystems in Mayan EDMS such as the OCR app
to determine how to interpret the document.

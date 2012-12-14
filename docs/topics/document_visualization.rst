======================
Document visualization
======================


On of the design philosophies of **Mayan EDMS** is avoid having users
download a documents and leave **Mayan EDMS** to be able to see them,
so in essence making **Mayan EDMS** a visualization tool too.
The conversion backend is a stack of functions,
first the mimetype is evaluated, if it is an office document it is passed
to LibreOffice_ working in headless mode (and managed by supervisor_)
for conversion to PDF_.  The PDF_ is stored in a temporary
cache along side all the other files that were not office documents,
from here they are inspected to determine the page count and the
corresponding blank database entires are created.  After the database
update they all go to the conversion driver specified by the configuration
option :setting:`CONVERTER_GRAPHICS_BACKEND` and a high resolution
master preview of each file is generated and stored in the persistent
cache.  From the master previews in the persistent cache, volatile
previews are then created on demand for the different sizes requested
(thumbnail, page preview, full preview) and rotated interactively
in the details view.

Office document conversion however won't always work as expected because
LibreOffice_ do not provide proper API's, so subprocess calling,
temporary files and other black magic needs to be invoked to get it
properly integrated.  **Mayan EDMS** treats documents as collections of pages
or frames, and text extraction and OCR is done per page not per document,
thats why even text documents need to be rendered by LibreOffice_
before they can be previewed and text can be extracted.  Just one
configuration option controls this conversion: :setting:`CONVERTER_LIBREOFFICE_PATH`

Version 0.12.1 introduced a new method of converting office documents, this
new method doesn't require the use of the command line utility ``UNOCONV``.
This new method proved to continue working better than previous solution
and the use of ``UNOCONV`` have been removed.  Existing conversion method
uses just one configuration option: :setting:`CONVERTER_LIBREOFFICE_PATH`


.. _PDF: http://en.wikipedia.org/wiki/Portable_Document_Format
.. _LibreOffice: http://www.libreoffice.org/
.. _supervisor: http://supervisord.org/introduction.html

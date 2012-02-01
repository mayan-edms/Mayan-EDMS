======================
Document visualization
======================


Mayan EDMS tries to avoid having users to download a document and leave
Mayan EDMS to be able to see them, so in essence making Mayan EDMS a
visualization tool too.  The conversion backend is a stack of functions,
first the mimetype is evaluated, if it is an office document it is passed
to libreoffice working in headless mode (and managed by supervisor)
via unoconv for conversion to PDF.  The PDF is stored in a temporary
cache along side all the other files that were not office documents,
from here they are inspected to determine the page count and the
corresponding blank database entires are created.  After the database
update they all go to the conversion driver specified by the user
(``python``, ``graphicsmagick``, imagemagick``) and a high resolution
master preview of each file is generated and stored in the persistent
cache.  From the master previews in the persistent cache, volatile
previews are then created on demand for the different sizes requested
(thumbnail, page preview, full preview) and rotate interactively
in the details view.

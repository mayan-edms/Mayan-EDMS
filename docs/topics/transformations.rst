===============
Transformations
===============

Transformation are persistent manipulations to the previews of the stored
documents. For example: a scanning equipment may only produce landscape PDFs.
In this case an useful transformation for that document source would be to
rotate all documents scanned by 270 degrees after being uploaded, this way
whenever a document is uploaded from that scanner it will appear in portrait
orientation. In this case add a this transformation to the Mayan EDMS source
that is connected to that device this way all pages scanned via that source
with inherit the transformation as they are created.

Transformations can also be added to existing documents, by clicking on a
document's page, then clicking on "transformations". In this view the Actions
menu will have a new option that reads "Create new transformation". At the
moment the rotation, zoom, crop, and resize transformations are available.
Once the document image has been corrected resubmit it for OCR for improved
results.

Transformations are not destructive and do not physically modify the document
file, they just modify the document's graphical representation.

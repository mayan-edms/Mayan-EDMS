===================
Document signatures
===================

**Mayan EDMS** supports two types of document signatures, these are embedded and 
detached signatures.  When a document with an embedded signature is 
uploaded, this signature is readily detected as part of the document 
inspection step.  If the public key corresponding to the signee of the 
document is not found, **Mayan EDMS** will try to obtain it from the list of 
keyserver specified in the config option :setting:`SIGNATURES_KEYSERVERS`.
Failing that, **Mayan EDMS** will indicate that the document is signed
but that it has no way to verify such signature.
Existing non signed documents can be signed in one of two way:  
by downloading the document, signing it, and uploading the signed document 
as a new version of the existing one using **Mayan EDMS** :doc:`versioning support <versioning>`
or by creating a detached signature for the non signed document and uploading 
such detached signature file using the option likewise named menu option.

Maintenance of the public keyring can be done using the ``Key management`` 
functionality in the ``Setup menu`` 

From this menu, key servers can be queried 
and the results imported.  Public keys no longer needed can also be deleted 
from this menu.

====================
Initial data loading
====================

Bulk document import
--------------------

**Mayan EDMS** has the ability to individually upload the contents of compressed 
files, however by nature of being a web based application it is bounded by the 
limitations of the HTTP protocol, this imposes a limit on the file size and 
the amount of time **Mayan EDMS** may keep a connection open while it processes 
compressed files.  When the desired amount of documents is bigger than what 
these limitations allow, **Mayan EDMS** provides a command line tool for out of 
process document importation.

The command line options for this feature are as follows::

  $ ./manage.py bulk_upload --noinput --metadata '{"project": "bulk"}' --document_type "Accounting documents" compressed.zip 

**Optional arguments**

* The ``--noinput`` argument skips confirmation and starts the upload immediately.
* The ``--metadata`` argument allows specifing what metadata will be assigned
  to the documents when uploaded.
* And the ``--document_type`` applies a previously defined 
  document type to the uploaded documents.


Bulk user import
----------------

As well as providing bulk document import functionality **Mayan EDMS** also
includes a management command to import a large number users
from a CSV file.  The command line options for this feature are as
follow::

  $ ./manage.py import_users --noinput --password=welcome123 --skip-repeated user_list.csv 

The CSV field order must be: username, first name, last name and email, any other 
column after those is ignored.

**Optional arguments**

* The ``--noinput`` argument skips confirmation and starts the import immediately.
* The ``--password`` argument allows specifing what default password will be assigned
  to all the new users that are imported.
* The ``--skip-repeated`` tells the importedr to not stop when finding
  that a user already exists in the database.

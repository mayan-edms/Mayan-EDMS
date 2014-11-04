====================
Initial data loading
====================

Bulk user import
----------------

As well as providing bulk document import functionality **Mayan EDMS** also
includes a management command to import a large number of users
from a CSV file.  The command line options for this feature are as
follow::

  $ mayan-edms.py import_users --noinput --password=welcome123 --skip-repeated user_list.csv

The CSV field order must be: username, first name, last name and email, any columns after
those are ignored.

**Optional arguments**

* The ``--noinput`` argument skips confirmation and starts the import immediately.
* The ``--password`` argument allows specifing what default password will be assigned
  to all the new users that are imported.
* The ``--skip-repeated`` tells the importer to not stop when finding
  that a user already exists in the database.

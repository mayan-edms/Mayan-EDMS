|Build Status| |Coverage Status| |PyPI badge| |Installs badge|

|Logo|

Mayan EDMS
==========

Free Open Source, Django based document management system with custom metadata
indexing, file serving integration, tagging, digital signature verification,
text parsing and OCR capabilities.

`Website`_

`Video demostration`_

`Documentation`_

`Translations`_

`Mailing list (via Google Groups)`_


License
-------

This project is open sourced under `Apache 2.0 License`_.

Installation
------------

To install **Mayan EDMS**, simply do:

.. code-block:: bash

    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install mayan-edms==1.0.rc1

Instead of using the usual ./manage.py use the alias mayan-edms.py:

.. code-block:: bash

    $ mayan-edms.py syncdb --migrate --noinput
    $ mayan-edms.py runserver

Point your browser to 127.0.0.1:8000 and use the automatically created admin
account.

Contribute
----------

- Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug.
- Fork `the repository`_ on GitHub to start making your changes to the **master** branch (or branch off of it).
- Write a test which shows that the bug was fixed or that the feature works as expected.
- Send a pull request
- Make sure to add yourself to the `contributors file`_.


.. _Website: http://www.mayan-edms.com
.. _Video demostration: http://bit.ly/pADNXv
.. _Documentation: http://readthedocs.org/docs/mayan/en/latest/
.. _Translations: https://www.transifex.com/projects/p/mayan-edms/
.. _Mailing list (via Google Groups): http://groups.google.com/group/mayan-edms
.. _Apache 2.0 License: https://www.apache.org/licenses/LICENSE-2.0.txt

.. |Build Status| image:: https://travis-ci.org/mayan-edms/mayan-edms.svg?branch=master
   :target: https://travis-ci.org/mayan-edms/mayan-edms
.. |Coverage Status| image:: https://coveralls.io/repos/mayan-edms/mayan-edms/badge.png?branch=master
   :target: https://coveralls.io/r/mayan-edms/mayan-edms?branch=master
.. |Logo| image:: https://github.com/rosarior/mayan/raw/master/docs/_static/mayan_logo_landscape_black.jpg
.. _`the repository`: http://github.com/mayan-edms/mayan-edms
.. _`contributors file`: https://github.com/mayan-edms/mayan-edms/blob/master/docs/credits/contributors.rst
.. |Installs badge| image:: https://pypip.in/d/mayan-edms/badge.png
   :target: https://crate.io/packages/mayan-edms/
.. |PyPI badge| image:: https://badge.fury.io/py/mayan-edms.png
   :target: http://badge.fury.io/py/mayan-edms

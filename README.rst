|Build Status| |Coverage Status| |PyPI badge| |Installs badge| |License badge| |Wheel badge|

|Logo|

Description
-----------

Free Open Source, Django based document management system with custom metadata
indexing, file serving integration, tagging, digital signature verification,
text parsing and OCR capabilities.

`Website`_

`Video demostration`_

`Documentation`_

`Translations`_

`Mailing list (via Google Groups)`_

|Animation|

License
-------

This project is open sourced under `Apache 2.0 License`_.

Installation
------------

To install **Mayan EDMS**, simply do:

.. code-block:: bash

    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install mayan-edms
    $ mayan-edms.py initialsetup
    $ mayan-edms.py runserver

Point your browser to 127.0.0.1:8000 and use the automatically created admin
account.

Contribute
----------

- Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug.
- Fork `the repository`_ on GitHub to start making your changes to the **development** branch (or branch off of it).
- Write a test which shows that the bug was fixed or that the feature works as expected.
- Add yourself to the `contributors file`_.
- Send a pull request


.. _Website: http://www.mayan-edms.com
.. _Video demostration: http://bit.ly/pADNXv
.. _Documentation: http://readthedocs.org/docs/mayan/en/latest/
.. _Translations: https://www.transifex.com/projects/p/mayan-edms/
.. _Mailing list (via Google Groups): http://groups.google.com/group/mayan-edms
.. _Apache 2.0 License: https://www.apache.org/licenses/LICENSE-2.0.txt
.. _`the repository`: http://github.com/mayan-edms/mayan-edms
.. _`contributors file`: https://github.com/mayan-edms/mayan-edms/blob/master/docs/topics/contributors.rst

.. |Build Status| image:: http://img.shields.io/travis/mayan-edms/mayan-edms/master.svg?style=flat
   :target: https://travis-ci.org/mayan-edms/mayan-edms
.. |Coverage Status| image:: http://img.shields.io/coveralls/mayan-edms/mayan-edms/master.svg?style=flat
   :target: https://coveralls.io/r/mayan-edms/mayan-edms?branch=master
.. |Logo| image:: https://github.com/mayan-edms/mayan-edms/raw/master/docs/_static/mayan_logo.png
.. |Animation| image:: https://github.com/mayan-edms/mayan-edms/raw/master/docs/_static/overview.gif
.. |Installs badge| image:: http://img.shields.io/pypi/dm/mayan-edms.svg?style=flat
   :target: https://crate.io/packages/mayan-edms/
.. |PyPI badge| image:: http://img.shields.io/pypi/v/mayan-edms.svg?style=flat
   :target: http://badge.fury.io/py/mayan-edms
.. |Wheel badge| image:: http://img.shields.io/badge/wheel-yes-green.svg?style=flat
.. |License badge| image:: http://img.shields.io/badge/license-Apache%202.0-green.svg?style=flat
.. |Analytics| image:: https://ga-beacon.appspot.com/UA-52965619-2/mayan-edms/readme?pixel

|Analytics|

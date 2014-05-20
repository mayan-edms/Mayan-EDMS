|Build Status| |Coverage Status|

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

Quick install
-------------

To bootstrap **Mayan EDMS** via the fabfile without having to clone
the entire repository, run the following command, replacing the part that
reads: with your current MySQL root password or the MySQL root password
you plan to assign to it, during the MySQL installation when executing the fabfile.

-  Debian or Ubuntu:

   cd /tmp && sudo apt-get install -y fabric wget tar gzip && wget
   https://github.com/mayan-edms/mayan-edms/raw/master/contrib/fabfile.tar.gz
   -O - \| tar -xvzf - && echo “database\_manager\_admin\_password=<Your
   MySQL root password>” > ~/.fabricrc && fab -H localhost install

-  Fedora:

   cd /tmp && sudo yum install -y fabric wget tar gzip && wget
   https://github.com/mayan-edms/mayan-edms/raw/master/contrib/fabfile.tar.gz
   -O - \| tar -xvzf - && echo “database\_manager\_admin\_password=<Your
   MySQL root password>” > ~/.fabricrc && fab -H localhost install

License
-------

This project is open sourced under `GNU GPL Version 3`_.


Contribute
----------

- Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug.
- Fork `the repository`_ on GitHub to start making your changes to the **master** branch (or branch off of it).
- Write a test which shows that the bug was fixed or that the feature works as expected.
- Send a pull request
- Make sure to add yourself to the `contributors file`_.


Donations
---------

Please `donate`_ if you are willing to support the further development
of this project.


.. _Website: http://www.mayan-edms.com
.. _Video demostration: http://bit.ly/pADNXv
.. _Documentation: http://readthedocs.org/docs/mayan/en/latest/
.. _Translations: https://www.transifex.net/projects/p/mayan-edms/
.. _Mailing list (via Google Groups): http://groups.google.com/group/mayan-edms
.. _GNU GPL Version 3: http://www.gnu.org/licenses/gpl-3.0.html
.. _donate: https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=W6LMMZHTNUJ6L

.. |Build Status| image:: https://travis-ci.org/mayan-edms/mayan-edms.svg?branch=master
   :target: https://travis-ci.org/mayan-edms/mayan-edms
.. |Coverage Status| image:: https://coveralls.io/repos/mayan-edms/mayan-edms/badge.png?branch=master
   :target: https://coveralls.io/r/mayan-edms/mayan-edms?branch=master
.. |Logo| image:: https://github.com/rosarior/mayan/raw/master/docs/_static/mayan_logo_landscape_black.jpg
.. _`the repository`: http://github.com/mayan-edms/mayan-edms
.. _`contributors file`: https://github.com/mayan-edms/mayan-edms/blob/master/docs/credits/contributors.rst

|pypi| |builds| |coverage| |python| |license|


.. image:: https://gitlab.com/mayan-edms/mayan-edms/raw/master/docs/_static/mayan_logo.png
    :align: center
    :width: 200
    :height: 200

Mayan EDMS is a document management system. Its main purpose is to store,
introspect, and categorize files, with a strong emphasis on preserving the
contextual and business information of documents. It can also OCR, preview,
label, sign, send, and receive thoses files. Other features of interest
are its workflow system, role based access control, and REST API.

.. image:: https://gitlab.com/mayan-edms/mayan-edms/raw/master/docs/_static/overview.gif
    :align: center


The easiest way to use Mayan EDMS is by using the official Docker_ image.
Make sure Docker is properly installed and working before attempting to install
Mayan EDMS.

With Docker properly installed, proceed to download the Mayan EDMS image using
the command:

.. code-block:: bash

    $ docker pull mayanedms/mayanedms:2.3

After the image finishes downloading, initialize a Mayan EDMS container.

.. code-block:: bash

    $ docker run -d --name mayan-edms --restart=always -p 80:80 \
    -v mayan_data:/var/lib/mayan mayanedms/mayanedms

Point your browser to the IP address 127.0.0.1 (or the alternate port chosen,
ie: 127.0.0.1:81) and use the automatically created admin account.

All files will be stored in the Docker volume ``mayan_data``

If another web server is running on port 80 use a different port in the ``-p``
option, ie: ``-p 81:80``.

For the complete set of installation, configuration, upgrade, and backup
instructions visit the Mayan EDMS Docker Hub page at:
https://hub.docker.com/r/mayanedms/mayanedms/

.. _Docker: https://www.docker.com/


Important links

- `Homepage <http://www.mayan-edms.com>`__
- `Videos <https://www.youtube.com/channel/UCJOOXHP1MJ9lVA7d8ZTlHPw>`__
- `Documentation <http://mayan.readthedocs.io/en/stable/>`__
- `Paid support <http://www.mayan-edms.com/providers/>`__
- `Roadmap <https://gitlab.com/mayan-edms/mayan-edms/wikis/roadmap>`__
- `Contributing <https://gitlab.com/mayan-edms/mayan-edms/blob/master/CONTRIBUTING.md>`__
- `Community forum <https://groups.google.com/forum/#!forum/mayan-edms>`__
- `Community forum archive <http://mayan-edms.1003.x6.nabble.com/>`__
- `Source code, issues, bugs <https://gitlab.com/mayan-edms/mayan-edms>`__
- `Plug-ins, other related projects <https://gitlab.com/mayan-edms/>`__
- `Translations <https://www.transifex.com/rosarior/mayan-edms/>`__



.. |pypi| image:: http://img.shields.io/pypi/v/mayan-edms.svg
   :target: http://badge.fury.io/py/mayan-edms
.. |builds| image:: https://gitlab.com/mayan-edms/mayan-edms/badges/master/build.svg
   :target: https://gitlab.com/mayan-edms/mayan-edms/pipelines
.. |coverage| image:: https://codecov.io/gitlab/mayan-edms/mayan-edms/coverage.svg?branch=master
   :target: https://codecov.io/gitlab/mayan-edms/mayan-edms?branch=master
.. |python| image:: https://img.shields.io/pypi/pyversions/mayan-edms.svg
.. |license| image:: https://img.shields.io/pypi/l/mayan-edms.svg?style=flat

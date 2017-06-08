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


The installation procedure uses the Docker container manager
(docker.com). Make sure Docker is properly installed and working before
attempting to install Mayan EDMS.

Step 1- Initialize the installation

.. code:: bash

    docker run --rm -v mayan_media:/var/lib/mayan \
    -v mayan_settings:/etc/mayan mayanedms/mayanedms mayan:init

Step 2- Deploy a container

.. code:: bash

    docker run -d --name mayan-edms --restart=always -p 80:80 \
    -v mayan_media:/var/lib/mayan -v mayan_settings:/etc/mayan mayanedms/mayanedms

Step 3- Open a browser and go to http://localhost


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

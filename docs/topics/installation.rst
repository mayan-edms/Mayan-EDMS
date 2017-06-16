Installation
============

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
    -v mayan_data:/var/lib/mayan mayanedms/mayanedms:2.3

Point your browser to the IP address 127.0.0.1 (or the alternate port chosen,
ie: 127.0.0.1:81) and use the automatically created admin account.

All files will be stored in the Docker volume ``mayan_data``

If another web server is running on port 80 use a different port in the ``-p``
option, ie: ``-p 81:80``.

For the complete set of installation, configuration, upgrade, and backup
instructions visit the Mayan EDMS Docker Hub page at:
https://hub.docker.com/r/mayanedms/mayanedms/

.. _Docker: https://www.docker.com/

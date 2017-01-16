Installation
============

The easiest way to use Mayan EDMS is by using the official Docker_ image.
Make sure Docker_ is properly installed and working before attempting to install
Mayan EDMS.

With Docker properly installed, proceed to download the Mayan EDMS image using
the command:

.. code-block:: bash

    docker pull mayanedms/mayanedms

After the image finishes downloading, initialize a Mayan EDMS container.

.. code-block:: bash

    docker run --rm -v mayan_media:/var/lib/mayan \
    -v mayan_settings:/etc/mayan mayanedms/mayanedms mayan:init

With initialization complete, launch the container. If another web server is
running on port 80 use a different port in the -p option, ie: -p 81:80.

.. code-block:: bash

    docker run -d --name mayan-edms --restart=always -p 80:80 \
    -v mayan_media:/var/lib/mayan -v mayan_settings:/etc/mayan \
    mayanedms/mayanedms

Point your browser to 127.0.0.1 (or the alternate port chosen, ie: 127.0.0.1:81)
and use the automatically created admin account.

All files will be stored in the following two volumes:

- mayan_media
- mayan_settings

Stopping and starting
---------------------
To stop the container use::

    docker stop mayan-edms

To start the container again::

    docker start mayan-edms

Configuring
-----------
To edit the settings file, check the physical location of the `mayan_settings`
volume using::

    docker volume inspect mayan_settings

Which should produce an output similar to this one:

.. code-block:: bash

    [
        {
            "Name": "mayan_settings",
            "Driver": "local",
            "Mountpoint": "/var/lib/docker/volumes/mayan_settings/_data",
            "Labels": null,
            "Scope": "local"
        }
    ]

In this case the physical location of the `mayan_settings` volume is
`/var/lib/docker/volumes/mayan_settings/_data`. Edit the settings file with your
favorite editor::

    sudo vi /var/lib/docker/volumes/mayan_settings/_data/local.py

Backups
-------

To backup the existing data, check the physical location of the `mayan_media`
volume using::

    docker volume inspect mayan_media

Which should produce an output similar to this one:

.. code-block:: bash

    [
        {
            "Name": "mayan_settings",
            "Driver": "local",
            "Mountpoint": "/var/lib/docker/volumes/mayan_media/_data",
            "Labels": null,
            "Scope": "local"
        }
    ]

Only the `db.sqlite3` file and the `document_storage` folder need to be backed
up::

    sudo tar -zcvf backup.tar.gz /var/lib/docker/volumes/mayan_media/_data/document_storage /var/lib/docker/volumes/mayan_media/_data/db.sqlite3
    sudo chown `whoami` backup.tar.gz

Restore
-------
Uncompress the archive in the original docker volume using::

    sudo tar -xvzf backup.tar.gz -C /


.. _Docker: https://www.docker.com/

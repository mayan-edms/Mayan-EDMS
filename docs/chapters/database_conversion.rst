*******************
Database conversion
*******************

Version 3.1.x added a new management command to help convert data residing in
an SQLite database to other database managers like PostgreSQL. Here is the
conversion procedure.

Direct install
==============

* Make a backup of your existing SQLite database and documents by copying the
  ``/opt/mayan-edms/media`` folder.
* :doc:`Upgrade to at least version 3.1.3. <../releases/3.1.3>`
*  Migrate the existing SQLite database with the command ``performupgrade``::

    sudo -u mayan MAYAN_MEDIA_ROOT=/opt/mayan-edms/media /opt/mayan-edms/bin/mayan-edms.py performupgrade

* Install PostgreSQL::

    sudo apt-get install postgresql libpq-dev

* Provision a PostgreSQL database::

    sudo -u postgres psql -c "CREATE USER mayan WITH password 'mayanuserpass';"
    sudo -u postgres createdb -O mayan mayan

* Install the Python client for PostgreSQL::

    sudo -u mayan /opt/mayan-edms/bin/pip install --no-cache-dir --no-use-pep517 psycopg2==2.7.3.2

* Copy the newly created fallback config file::

    cp /opt/mayan-edms/media/config_backup.yml /opt/mayan-edms/media/config.yml

* Edit the configuration file to add the entry for the PostgreSQL database and
  rename the SQLite database to 'old'::

    # Before
    DATABASES:
      default:
        ATOMIC_REQUESTS: false
        AUTOCOMMIT: true
        CONN_MAX_AGE: 0
        ENGINE: django.db.backends.sqlite3
        HOST: ''
        NAME: /opt/mayan-edms/media/db.sqlite3
        OPTIONS: {}
        PASSWORD: ''
        PORT: ''
        TEST: {CHARSET: null, COLLATION: null, MIRROR: null, NAME: null}
        TIME_ZONE: null
        USER: ''

    # After
    DATABASES:
      old:
        ATOMIC_REQUESTS: false
        AUTOCOMMIT: true
        CONN_MAX_AGE: 0
        ENGINE: django.db.backends.sqlite3
        HOST: ''
        NAME: /opt/mayan-edms/media/db.sqlite3
        OPTIONS: {}
        PASSWORD: ''
        PORT: ''
        TEST: {CHARSET: null, COLLATION: null, MIRROR: null, NAME: null}
        TIME_ZONE: null
        USER: ''
      default:
        ATOMIC_REQUESTS: false
        AUTOCOMMIT: true
        CONN_MAX_AGE: 0
        ENGINE: django.db.backends.postgresql
        HOST: '127.0.0.1'
        NAME: /opt/mayan-edms/media/db.sqlite3
        OPTIONS: {}
        PASSWORD: 'mayanuserpass'
        PORT: ''
        TEST: {CHARSET: null, COLLATION: null, MIRROR: null, NAME: null}
        TIME_ZONE: null
        USER: 'mayan'

* Migrate the new database to create the empty tables::

    sudo -u mayan MAYAN_DATABASE_ENGINE=django.db.backends.postgresql MAYAN_DATABASE_NAME=mayan MAYAN_DATABASE_PASSWORD=mayanuserpass MAYAN_DATABASE_USER=mayan MAYAN_DATABASE_HOST=127.0.0.1 MAYAN_MEDIA_ROOT=/opt/mayan-edms/media /opt/mayan-edms/bin/mayan-edms.py migrate

* Convert the data in the SQLite and store it in the PostgreSQL database::

    sudo -u mayan MAYAN_DATABASE_ENGINE=django.db.backends.postgresql MAYAN_DATABASE_NAME=mayan MAYAN_DATABASE_PASSWORD=mayanuserpass MAYAN_DATABASE_USER=mayan MAYAN_DATABASE_HOST=127.0.0.1 MAYAN_MEDIA_ROOT=/opt/mayan-edms/media /opt/mayan-edms/bin/mayan-edms.py convertdb --from=old --to=default --force

* Update the supervisor config file to have Mayan EDMS run from the PostgreSQL database::

    [supervisord]
    environment=
        <...>
        MAYAN_DATABASE_ENGINE=django.db.backends.postgresql,
        MAYAN_DATABASE_HOST=127.0.0.1,
        MAYAN_DATABASE_NAME=mayan,
        MAYAN_DATABASE_PASSWORD=mayanuserpass,
        MAYAN_DATABASE_USER=mayan,
        MAYAN_DATABASE_CONN_MAX_AGE=360,
        <...>

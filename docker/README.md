[![Docker pulls](https://img.shields.io/docker/pulls/mayanedms/mayanedms.svg?maxAge=3600)](https://hub.docker.com/r/mayanedms/mayanedms/) [![Docker Stars](https://img.shields.io/docker/stars/mayanedms/mayanedms.svg?maxAge=3600)](https://hub.docker.com/r/mayanedms/mayanedms/) [![Docker layers](https://images.microbadger.com/badges/image/mayanedms/mayanedms.svg)](https://microbadger.com/images/mayanedms/mayanedms) [![Docker version](https://images.microbadger.com/badges/version/mayanedms/mayanedms.svg)](https://microbadger.com/images/mayanedms/mayanedms) ![Docker build](https://img.shields.io/docker/automated/mayanedms/mayanedms.svg) ![License](https://img.shields.io/badge/License-MIT-green.svg?maxAge=3600)

# Quick reference

-   **Where to get help**:
    [the Docker Community Forums](https://forums.docker.com/), [the Docker Community Slack](https://blog.docker.com/2016/11/introducing-docker-community-directory-docker-community-slack/), or [Stack Overflow](https://stackoverflow.com/search?tab=newest&q=docker)

-   **Where to file issues**:
    [https://gitlab.com/mayan-edms/mayan-edms-docker/issues](https://gitlab.com/mayan-edms/mayan-edms-docker/issues)

-   **Maintained by**:
    [Roberto Rosario](https://gitlab.com/rosarior)

-   **Supported Docker versions**:
    [the latest release](https://github.com/docker/docker/releases/latest) (down to 1.12 on a best-effort basis)

# What is Mayan EDMS?

Mayan EDMS, often simply "Mayan", is an electronic document management system with an emphasis on automation.

As a document manager its main purpose is to store, introspect, and categorize files, with a strong emphasis on preserving the contextual and business information of documents. It also provide means to ease retrieval, as requested by users or other software applications, be it those on the same computer or those running on another computer across a network (including the Internet). It can handle workloads ranging from small single-machine applications to large enterprise applications with many concurrent users. It can also OCR, preview, label, sign, send, and receive documents. Other features of interest are its workflow system, role based access control, and REST API.

> [wikipedia.org/wiki/Mayan_(software)](https://en.wikipedia.org/wiki/Mayan_%28software%29)

![logo](https://gitlab.com/mayan-edms/mayan-edms/raw/master/docs/_static/mayan_logo.png)

# How to use this image

## Start a Mayan EDMS instance

With Docker properly installed, proceed to download the Mayan EDMS image using the command:

```console
$ docker pull mayanedms/mayanedms:2.7.3
```

```console
$ docker run -d --name mayan-edms --restart=always -p 80:80 -v mayan_data:/var/lib/mayan mayanedms/mayanedms:2.7.3
```

The container will be available by browsing to [http://localhost](http://localhost)

All files will be stored in the volume ``mayan_data``

If another web server is running on port 80 use a different port in the ``-p`` option, ie: ``-p 81:80``.


## Stopping and starting the container

To stop the container use:

```console
$ docker stop mayan-edms
```

To start the container again:

```console
$ docker start mayan-edms
```

## Configuration

To edit the settings file, check the physical location of the ``mayan_data`` volume using:

```console
$ docker volume inspect mayan_data
```

Which should produce an output similar to this one:

```console
    [
        {
            "Name": "mayan_data",
            "Driver": "local",
            "Mountpoint": "/var/lib/docker/volumes/mayan_data/_data",
            "Labels": null,
            "Scope": "local"
        }
    ]
```

In this case the physical location of the ``mayan_data`` volume is ``/var/lib/docker/volumes/mayan_data/_data``. The settings file to change is named ``settings/local.py`` inside this volume. Edit the settings with your favorite editor, example:

```console
$ sudo vi /var/lib/docker/volumes/mayan_data/_data/settings/local.py
```

Stop and start the container again for the changes to take effect.


## Environment Variables

The Mayan EDMS image uses several environment variables. While none of the variables are required, they may significantly aid you in using the image.

### `MAYAN_DATABASE_DRIVER`

Defaults to ``None``. This environment variable configures the database backend to use. If left unset, SQLite will be used. The database backends supported by this Docker image are:

- 'django.db.backends.postgresql'
- 'django.db.backends.mysql'
- 'django.db.backends.sqlite3' same as ``None``

When using the SQLite backend, the database file will be saved in the ``mayan_data`` volume.


### `MAYAN_DATABASE_NAME`

Defaults to 'mayan'. This optional environment variable can be used to define the database name that Mayan EDMS will connect to. For more information read the pertinent Django documentation page: [Connecting to the database](https://docs.djangoproject.com/en/1.10/ref/databases/#connecting-to-the-database)


### `MAYAN_DATABASE_USER`

Defaults to 'mayan'. This optional environment variable is used to set the username that will be used to connect to the database. For more information read the pertinent Django documentation page: [Settings, USER](https://docs.djangoproject.com/en/1.10/ref/settings/#user)

### `MAYAN_DATABASE_PASSWORD`

Defaults to ''. This optional environment variable is used to set the password that will be used to connect to the database. For more information read the pertinent Django documentation page: [Settings, PASSWORD](https://docs.djangoproject.com/en/1.10/ref/settings/#password)

### `MAYAN_DATABASE_HOST`

Defaults to `None`. This optional environment variable is used to set the hostname that will be used to connect to the database. This can be the hostname of another container or an IP address. For more information read the pertinent Django documentation page: [Settings, HOST](https://docs.djangoproject.com/en/1.10/ref/settings/#host)

### `MAYAN_DATABASE_PORT`

Defaults to `None`. This optional environment variable is used to set the port number to use when connecting to the database. An empty string means the default port. Not used with SQLite. For more information read the pertinent Django documentation page: [Settings, PORT](https://docs.djangoproject.com/en/1.11/ref/settings/#port)

### `MAYAN_BROKER_URL`

Defaults to 'redis://127.0.0.1:6379/0'. This optional environment variable is determines the broker that Celery will use to relay task messages between the frontend code and the background workers. For more information read the pertinent Celery Kombu documentation page: [Broker URL](http://kombu.readthedocs.io/en/latest/userguide/connections.html#connection-urls)

This Docker image supports using Redis and RabbitMQ as brokers.

Caveat: If the `MAYAN_BROKER_URL` and `MAYAN_CELERY_RESULT_BACKEND` environment variables are specified, the built-in Redis server inside the container will be disabled.

### `MAYAN_CELERY_RESULT_BACKEND`

Defaults to 'redis://127.0.0.1:6379/0'. This optional environment variable is determines the results backend that Celery will use to relay result messages between from the background workers to the frontend code. For more information read the pertinent Celery Kombu documentation page: [Task result backend settings](http://docs.celeryproject.org/en/3.1/configuration.html#celery-result-backend)

This Docker image supports using Redis and RabbitMQ as result backends.

Caveat: If the `MAYAN_BROKER_URL` and `MAYAN_CELERY_RESULT_BACKEND` environment variables are specified, the built-in Redis server inside the container will be disabled.

### `MAYAN_NGINX_CLIENT_MAX_BODY_SIZE`

Defaults to '500M'. Sets the maximum allowed size of the client request body, specified in the “Content-Length” request header field. If the size in a request exceeds the configured value, the 413 (Request Entity Too Large) error is returned to the client. Please be aware that browsers cannot correctly display this error. Setting size to 0 disables checking of client request body size. Increase this if you are uploading files bigger than the default 500 megabytes.

### `MAYAN_NGINX_PROXY_READ_TIMEOUT`

Defaults to '600s'. Defines a timeout for reading a response from the proxied server. The timeout is set only between two successive read operations, not for the transmission of the whole response. If the proxied server does not transmit anything within this time, the connection is closed. This means that this is the maximum amount of time NGINX will wait for a connection Mayan EDMS to complete before returning an error. Increase this if you are uploading files that take more than the default 600 seconds to transfer.

### `MAYAN_SETTINGS_LOCAL_STRING`

Optional. Allows customizing the initial settings/local.py from the text content of the variable.

### `MAYAN_SETTINGS_LOCAL_FILE`

Optional. Allows customizing the initial settings/local.py from the text content of the file pointed by the variable.

## Other defaults

When using external database containers by means of the `MAYAN_DATABASE_NAME` environment variable, the database settings will add Django's option to keep connections alive for 60 seconds. For more information read the pertinent Django documentation page: [Settings, CONN_MAX_AGE](https://docs.djangoproject.com/en/1.10/ref/settings/#conn-max-age)


## Accessing outside data

To use Mayan EDMS's staging folders or watch folders from Docker, the data for these source must be made accessible to the container. This is done by mounting the folders in the host computer to folders inside the container. This is necessary because Docker containers do not have access to host data on purpose. For example, to make a folder in the host accessible as a watch folder, add the following to the Docker command line when starting the container:

```console
-v /opt/scanned_files:/srv/watch_folder
```

The complete command line would then be:

```console
$ docker run -d --name mayan-edms --restart=always -p 80:80 -v mayan_data:/var/lib/mayan -v /opt/scanned_files:/srv/watch_folder mayanedms/mayanedms:2.7.3
```

Now create a watch folder in Mayan EDMS using the path `/srv/watch_folder` and
the documents from the host folder `/opt/scanned_files` will be automatically
available. Use the same procedure to mount host folders to be used as staging
folders. In this example `/srv/watch_folder` was as the container directory,
but any path can be used as long as it is not an already existing path or a
path used by any other program.


## Performing backups

To backup the existing data, check the physical location of the ``mayan_data`` volume using:

```console
$ docker volume inspect mayan_data
```

Which should produce an output similar to this one:

```console
    [
        {
            "Name": "mayan_data",
            "Driver": "local",
            "Mountpoint": "/var/lib/docker/volumes/mayan_data/_data",
            "Labels": null,
            "Scope": "local"
        }
    ]
```

Only the ``db.sqlite3`` file, the ``document_storage`` and ``settings`` folders need to be backed up:

```console
$ sudo tar -zcvf backup.tar.gz /var/lib/docker/volumes/mayan_data/_data/document_storage /var/lib/docker/volumes/mayan_data/_data/settings /var/lib/docker/volumes/mayan_data/_data/db.sqlite3
$ sudo chown `whoami` backup.tar.gz
```

If an external PostgreSQL or MySQL database or database containers, these too need to be backed up using their respective procedures.


## Restoring from a backup

Uncompress the backup archive in the original docker volume using:

```console
$ sudo tar -xvzf backup.tar.gz -C /
```

## Upgrading

Upgrading a Mayan EDMS Docker container is actually a matter of stopping and deleting the container, downloading the most recent version of the image and starting a container again. The container will take care of updating the database structure to the newest version if necessary.

**IMPORTANT!** Do not delete the volume `mayan_data`, only the container.

Stop the container to be upgraded:

```console
$ docker stop mayan-edms
```

Remove the container:

```console
$ docker rm mayan-edms
```

Pull the new image version:

```console
$ docker pull mayanedms/mayanedms:2.7.3
```

Start the container again with the new image version:

```console
$ docker run -d --name mayan-edms --restart=always -p 80:80 -v mayan_data:/var/lib/mayan mayanedms/mayanedms:2.7.3
```

### Upgrading from a version 2.1 or earlier.

Previous Mayan EDMS Docker images used two volumes, one for data, and the other for settings. These volumes are now consolidated into one. If you are upgrading from a version 2.1 or earlier Mayan EDMS Docker container, you need to merge the files of these containers into one.

Stop the container to be upgraded:

```console
$ docker stop mayan-edms
```

Remove the container:

```console
$ docker rm mayan-edms
```

Pull the new image version:

```console
$ docker pull mayanedms/mayanedms:2.7.3
```

Create a new volume that will hold the contents of the ``mayan_media`` and the ``mayan_settings`` volumes.

```console
$ docker volume create mayan_data
```

Check the physical location of the ``mayan_data`` volume using:

```console
$ docker volume inspect mayan_data
```

Which should produce an output similar to this one:

```console
    [
        {
            "Name": "mayan_data",
            "Driver": "local",
            "Mountpoint": "/var/lib/docker/volumes/mayan_data/_data",
            "Labels": null,
            "Scope": "local"
        }
    ]
```

Copy the old SQLite database and document files to the new volume.

```console
$ sudo cp -r /var/lib/docker/volumes/mayan_media/_data/* /var/lib/docker/volumes/mayan_data/_data/
```

Create a folder for the settings in the new volume.

```console
$ sudo mkdir /var/lib/docker/volumes/mayan_data/_data/settings
```

Create two empty `__init__.py` files. One in the top folder of the new volume.

```console
$ sudo touch /var/lib/docker/volumes/mayan_data/_data/__init__.py
```

And the other in the settings folder of the new volume.

```console
$ sudo touch /var/lib/docker/volumes/mayan_data/_data/settings/__init__.py
```

Create a `base.py` file in the settings folder of the new volume.

```console
$ sudo cat << EOF > /var/lib/docker/volumes/mayan_data/_data/settings/base.py
# Empty base.py to allow local.py to run
from mayan.settings.docker import *  # NOQA
EOF
```

Copy the `local.py` settings file from the old `mayan_settings` volume to the new `mayan_data` volume.

```console
$ sudo cp /var/lib/docker/volumes/mayan_settings/_data/local.py /var/lib/docker/volumes/mayan_data/_data/settings/
```

Launch a container with the new version of the Docker image using the new `mayan_data` volume.

```console
$ docker run -d --name mayan-edms --restart=always -p 80:80 -v mayan_data:/var/lib/mayan mayanedms/mayanedms:2.7.3
```

Verify that all your previous documents are present and accesible. Delete the old volumes using:

```console
$ docker volume rm mayan_media
```

```console
$ docker volume rm mayan_settings
```

### Upgrading from version 2.2.

Perform all the steps above as if upgrading from a version 2.1 or earlier, up to the step copying the `local.py` file, the step before launching of a container using then new image version.

Edit the `local.py` settings file and delete all lines, leaving only the lines:

```console
from __future__ import absolute_import

from .base import *
SECRET_KEY = '< keep your random secret key >'
```

This is necessary because version 2.2 included experimental support for Postgres as a database backend. Now that Postgres support has been made standard, the custom configuration lines that version 2.2 added to the `local.py` file are not necesary and need to be removed to avoid configuration conflicts.

Save the file and launch a container using the new version.

```console
$ docker run -d --name mayan-edms --restart=always -p 80:80 -v mayan_data:/var/lib/mayan mayanedms/mayanedms:2.7.3
```

Verify that all your previous documents are present and accesible. Delete the old volumes using:

```console
$ docker volume rm mayan_media
```

```console
$ docker volume rm mayan_settings
```

## Building the image

Clone the repository with:

```console
$ git clone https://gitlab.com/mayan-edms/mayan-edms-docker.git
```

Change to the directory of the cloned repository:

```console
$ cd mayan-edms-docker
```

Execute Docker's build command:

```console
$ docker build -t mayanedms/mayanedms:2.7.3 .
```

Or using an apt cacher to speed up the build:

```console
$ docker build -t mayanedms/mayanedms:2.7.3 --build-arg APT_PROXY=172.17.0.1:3142 .
```

Replace the IP address `172.17.0.1` with the IP address of the Docker host used from which these commands are running.


## Customizing the image

### Simple method

If you just need to add a few Ubuntu or Python packages to your installation,
you can use the following environment variables::

**`MAYAN_APT_INSTALLS`**

Specifies a list of Ubuntu .deb packages to be installed via APT when the
container is first created. The installed packages are not lost when the image
is stopped. Example: To install the Tesseract OCR language packs for German
and Spanish add the following in your `docker start` command line:

```console
-e MAYAN_APT_INSTALLS="tesseract-ocr-deu tesseract-ocr-spa"
```

**`MAYAN_PIP_INSTALLS`**

Specifies a list of Python packages to be installed via `pip`. Packages will be
downloaded from the Python Package Index (https://pypi.python.org) by default.
If you need to use local packages, copy them to the folder `/pip_installs` in
the `mayan_data` volume and specify their full path in the environment variable.
Example: To install Werkzeug fromt the web and your local Python package, copy
you local Python package before running a new container with:

```console
$ sudo cp my_package.whl /var/lib/docker/volumes/mayan_data/_data/pip_installs/
```

If the folder `pip_installs` doesn't exists because you are upgrading from a
previous version you can create it with:

```console
$ sudo mkdir /var/lib/docker/volumes/mayan_data/_data/pip_installs/
```

Then specify `Werkzeug` and you local package's path in the environment variable.
The path to the local package will be `/var/lib/mayan/pip_installs` because is
where the `mayan_data` volume is mounted:


```console
-e MAYAN_PIP_INSTALLS="Werkzeug /var/lib/mayan/pip_installs/my_package.whl"
```

### Advanced method

Use this method when you need to change more things in the default image than
just Ubuntu or Python packages.

As an example, let's create a new image that adds German OCR support.

Create a file name `Dockerfile`. This will create a new local image of Mayan EDMS that builds on top of the official image. This is how Docker works, by layering images. Create a new file called `Dockerfile.local` with the following content:

*Dockerfile.local*

```console
    # Custom Dockerfile to add German OCR library
    # This Dockerfile uses the official Mayan EDMS image
    # as a base.

    FROM mayanedms/mayanedms:2.7.3

    ENV DEBIAN_FRONTEND noninteractive

    # Install Ubuntu German OCR package and clean up afterwards

    RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    tesseract-ocr-deu \
    && \
    apt-get clean autoclean && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/* && \
    rm -f /var/cache/apt/archives/*.deb

    # Retain the original entrypoint and command
    ENTRYPOINT ["entrypoint.sh"]
    CMD ["mayan"]
```

Now proceed to build your own custom image with the following command:

```console
$ docker build -t my_images/mayanedms -f Dockerfile.local .
```

Then use all the normal subsequent commands, changing every instance of `mayanedms/mayanedms` to `my_images/mayanedms`.

## Testing

Start a Vagrant box from the include Vagrant file. This Vagrant box will builds the Docker image and then start a container:

```console
$ vagrant up
```

Create the same Vagrant box using an apt cacher to speed up the build:

```console
$ APT_PROXY=172.17.0.1:3142 vagrant up
```

Replace the IP address `172.17.0.1` with the IP address of the Docker host used from which these commands are running.

## Using Docker compose

To deploy a complete production stack using the included Docker compose file execute:

```console
$ docker-compose -f docker-compose.yml up -d
```

This Docker compose file will provision four containers:

- Postgres as the database
- Redis as the Celery result storage
- RabbitMQ as the Celery broker
- Mayan EDMS using the above service containers

To stop the stack use:

```console
$ docker-compose -f docker-compose.yml stop
```

The stack will also create four volumes to store the data of each container. These are:

- mayan_app - The Mayan EDMS data container, normally called `mayan_data` when not using Docker compose.
- mayan_broker - The broker volume, in this case RabbitMQ.
- mayan_db - The database volume, in this case Postgres.
- mayan_results - The celery result backend volume, in this case Redis.

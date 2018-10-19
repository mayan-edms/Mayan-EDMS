**************
Object storage
**************

It is possible to use object storage instead of the default filesystem based
storage. One such object storage system is Amazon S3 (Simple Storage Service)
API compatible object storage. The following steps will configure Mayan EDMS
to use a S3 style storage for documents.

1. Install the django-storages and boto3 Python libraries.

  * For the direct deployment method of installation use::

        pip install django-storages boto3


  * or if using the Docker image, add the following the command line that runs the container::

    -e MAYAN_PIP_INSTALLS='django-storages boto3'


2. From the web interface navigate to the :menuselection:`System --> Setup --> Setting --> Documents` menu.
3. Locate the **DOCUMENTS_STORAGE_BACKEND** setting, press **Edit** and enter::

    storages.backends.s3boto3.S3Boto3Storage

4. Save and locate the setting **DOCUMENTS_STORAGE_BACKEND_ARGUMENTS**, press **Edit** and enter::

    '{access_key: <your S3 access key>, secret_key: <your S3 secret key>, bucket_name: <S3 bucket name>}'

5. Save and restart your Mayan EDMS installation for the setting to take effect.


Storage
=======
Mayan EDMS stores documents in their original file format only changing the
filename to avoid collision. For best input and output speed use a block
based local filesystem for the ``/media`` sub folder of the path specified by
the MEDIA_ROOT setting. For increased storage capacity use an object storage
filesystem like S3.

To use a S3 compatible object storage do the following:

* Install the Python packages ``django-storages`` and ``boto3``:

  * Using Python::

      pip install django-storages boto3

  * Using Docker::

    -e MAYAN_PIP_INSTALLS='django-storages boto3'

On the Mayan EDMS user interface, go to ``System``, ``Setup``, ``Settings``,
``Documents`` and change the following setting:

* ``DOCUMENTS_STORAGE_BACKEND`` to ``storages.backends.s3boto3.S3Boto3Storage``
* ``DOCUMENTS_STORAGE_BACKEND_ARGUMENTS`` to ``'{access_key: <your access key>, secret_key: <your secret key>, bucket_name: <bucket name>}'``.

Restart Mayan EDMS for the changes to take effect.

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

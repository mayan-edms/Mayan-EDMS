.. _development:

Development
===========

Mayan EDMS is under active development, and contributions are welcome.

If you have a feature request, suggestion or bug report, please open a new
issue on the `GitLab issue tracker`_. To submit patches, please send a merge
request on GitLab_.

.. _GitLab: https://gitlab.com/mayan-edms/mayan-edms/
.. _`GitLab issue tracker`: https://gitlab.com/mayan-edms/mayan-edms/issues


Project philosophies
--------------------

How to think about Mayan EDMS when doing changes or adding new features,
why things are the way they are in Mayan EDMS.

- Functionality must be as market/sector independent as possible, code for the
  95% of use cases.
- Each user must be able to configure and customize it to their needs after
  install.
- Abstract as much as possible, each app must be an expert in just one thing,
  for other things they should use the API/classes/functions of other apps.
- Assume as little as possible about anything outside the project
  (hardware, OS, storage).
- Provide Python based abstraction so that a default install runs with a single
  step.
- No hard dependencies on binaries unless there is no other choice.
- Provide “drivers” or switchable backends to allow users to fine tune the
  installation.
- Call to binaries only when there is no other choice or the Python choices are
  not viable/mature/efficient.
- Each app is as independent and self contained as possible. Exceptions, the
  basic requirements: navigation, permissions, common, main.
- If an app is meant to be used by more than one other app it should be as
  generic as possible in regard to the project and another app will bridge the functionality.

  - Example: since indexing (document_indexing) only applies to documents, the
    app is specialized and depends on the documents app.


Coding conventions
------------------

Follow PEP8
~~~~~~~~~~~
Whenever possible, but don't obsess over things like line length.

.. code-block:: bash

    $ flake8 --ignore=E501,E128,E122 |less

Imports
~~~~~~~

Import order should be:

- Standard Python modules
- Installed Python modules
- Core Django modules
- Installed Django modules
- Mayan EDMS modules
- Local imports

Example:

.. code-block:: bash

    from __future__ import absolute_import

    # Standard Python library
    import base64

    # 3rd party installed Python libraries
    import requests

    # Django core modules
    from django.db.models import Q
    from django.template.defaultfilters import slugify
    from django.utils.translation import ugettext
    from django.utils.translation import ugettext_lazy as _

    # 3rd party installed Django libraries
    from rest_framework import APIView

    # Mayan apps
    from metadata.classes import MetadataClass

    # Local app imports (relative)
    from .conf.settings import (
        AVAILABLE_INDEXING_FUNCTIONS,
        MAX_SUFFIX_COUNT, SLUGIFY_PATHS
    )
    from .exceptions import MaxSuffixCountReached
    from .filesystem import (
        fs_create_index_directory, fs_create_document_link,
        fs_delete_document_link, fs_delete_index_directory,
        assemble_suffixed_filename
    )
    from .models import Index, IndexInstanceNode, DocumentRenameCount

All local app module imports are in relative form, local app module name is to
be referenced as little as possible, unless required by a specific feature,
trick, restriction, ie: Runtime modification of the module's attributes.

Incorrect:

.. code-block:: bash


    # documents app views.py model
    from documents.models import Document

Correct:

.. code-block:: bash

    # documents app views.py model
    from .models import Document


Dependencies
~~~~~~~~~~~~
Mayan EDMS apps follow a hierarchical model of dependency. Apps import from
their parents or siblings, never from their children. Think plugins. A parent
app must never assume anything about a possible existing child app. The
documents app and the Document model are the basic entities they must never
import anything else. The common and main apps are the base apps.


Variables
~~~~~~~~~
Naming of variables should follow a Major to Minor convention, usually
including the purpose of the variable as the first piece of the name, using
underscores as spaces. camelCase is not used in Mayan EDMS.

Examples:

Links:

.. code-block:: bash

    link_document_page_transformation_list = ...
    link_document_page_transformation_create = ...
    link_document_page_transformation_edit = ...
    link_document_page_transformation_delete = ...

Constants:

.. code-block:: bash

    PERMISSION_SMART_LINK_VIEW = ...
    PERMISSION_SMART_LINK_CREATE = ...
    PERMISSION_SMART_LINK_DELETE = ...
    PERMISSION_SMART_LINK_EDIT = ...

Classes:

.. code-block:: bash

    class Document(models.Model):
    class DocumentPage(models.Model):
    class DocumentPageTransformation(models.Model):
    class DocumentType(models.Model):
    class DocumentTypeFilename(models.Model):


Strings
~~~~~~~
Quotation character used in Mayan EDMS for strings is the single quote.
Double quote is used for multiple line comments or HTML markup.

Migrations
~~~~~~~~~~
Migrations should do only one thing (eg: either create a table, move data to a
new table or remove an old table) to aid retrying on failure.

General
~~~~~~~
Code should appear in their modules in alphabetic order or in their order of
importance if it makes more sense for the specific application. This makes
visual scanning easier on modules with a large number of imports, views or
classes. Class methods that return a value should be pretended with a
``get_`` to differentiate from an object’s properties. When a variable refers
to a file it should be named as follows:

- filename:  The file’s name and extension only.
- filepath:  The entire path to the file including the filename.
- path:  A path to a directory.

Flash messages should end with a period as applicable for the language.
Only exception is when the tail of the message contains an exceptions message
as passed directly from the exception object.

Source Control
--------------

Mayan EDMS source is controlled with Git_.

The project is publicly accessible, hosted and can be cloned from **GitLab** using::

    git clone https://gitlab.com/mayan-edms/mayan-edms.git


Git branch structure
--------------------

Mayan EDMS follows a simplified model layout based on Vincent Driessen's
`Successful Git Branching Model`_ blog post.

``develop``
    The "next release" branch, likely unstable.
``master``
    Current production release (|version|).
``feature/``
    Unfinished/unmerged feature.
``series/``
    Released versions.


Each release is tagged separately.

When submitting patches, please place your code in its own ``feature/`` branch
prior to opening a Merge Request on GitLab_.

.. _Git: http://git-scm.org
.. _`Successful Git Branching Model`: http://nvie.com/posts/a-successful-git-branching-model/


Steps to deploy a development version
-------------------------------------
.. code-block:: bash

    git clone https://gitlab.com/mayan-edms/mayan-edms.git
    cd mayan-edms
    git checkout development
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ./manage.py initialsetup
    ./manage.py runserver


Setting up a development version using Vagrant
----------------------------------------------
Make sure you have Vagrant and a provider properly installed as per
https://docs.vagrantup.com/v2/installation/index.html

Start and provision a machine using:

.. code-block:: bash

    vagrant up development

To launch a standalone development server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    vagrant ssh
    vagrant@vagrant-ubuntu-trusty-32:~$ cd ~/mayan-edms/
    vagrant@vagrant-ubuntu-trusty-32:~$ source venv/bin/activate
    vagrant@vagrant-ubuntu-trusty-32:~$ ./manage.py runserver 0.0.0.0:8000

To launch a development server with a celery worker and Redis as broker
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    vagrant ssh
    vagrant@vagrant-ubuntu-trusty-32:~$ cd ~/mayan-edms/
    vagrant@vagrant-ubuntu-trusty-32:~$ source venv/bin/activate
    vagrant@vagrant-ubuntu-trusty-32:~$ ./manage.py runserver 0.0.0.0:8000 --settings=mayan.settings.celery_redis

Then on a separate console launch a celery worker from the same provisioned Vagrant machine:

.. code-block:: bash

    vagrant ssh
    vagrant@vagrant-ubuntu-trusty-32:~$ cd ~/mayan-edms/
    vagrant@vagrant-ubuntu-trusty-32:~$ source venv/bin/activate
    vagrant@vagrant-ubuntu-trusty-32:~$ DJANGO_SETTINGS_MODULE='mayan.settings.celery_redis' celery -A mayan worker -l DEBUG -Q checkouts,mailing,uploads,converter,ocr,tools,indexing,metadata -Ofair -B


Contributing changes
--------------------
Once your have created and committed some new code or feature, submit a Pull
Request. Be sure to merge with the development branch before doing a Pull
Request so that patches apply as cleanly as possible. If there are no conflicts,
Merge Requests can be merged directly from the website UI otherwise a manual
command line merge has to be done and your patches might take longer to get
merged.


Debugging
---------

Mayan EDMS makes extensive use of Django's new `logging capabilities`_.
By default debug logging for all apps is turned on. If you wish to customize
how logging is managed turn off automatic logging by setting
`COMMON_AUTO_LOGGING` to ``False`` and add the following lines to your
``settings/local.py`` file::

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(name)s %(process)d %(thread)d %(message)s'
            },
            'intermediate': {
                'format': '%(name)s <%(process)d> [%(levelname)s] "%(funcName)s() %(message)s"'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'handlers': {
            'console':{
                'level':'DEBUG',
                'class':'logging.StreamHandler',
                'formatter': 'intermediate'
            }
        },
        'loggers': {
            'documents': {
                'handlers':['console'],
                'propagate': True,
                'level':'DEBUG',
            },
            'common': {
                'handlers':['console'],
                'propagate': True,
                'level':'DEBUG',
            },
        }
    }


Likewise, to see the debug output of the ``tags`` app, just add the following inside the ``loggers`` block::


    'tags': {
        'handlers':['console'],
        'propagate': True,
        'level':'DEBUG',
    },


.. _`logging capabilities`: https://docs.djangoproject.com/en/dev/topics/logging


Documentation
-------------

The documentation is written in `reStructured Text`_ format, processed with
Sphinx_, and resides in the ``docs`` directory. In order to build it, you will
first need to install the documentation editing dependencies with::

    pip install -r requirements/documentation.txt

Then, to build an HTML version of the documentation, run the following command
from the **docs** directory::

    make livehtml

The generated documentation can be viewed by browsing to http://127.0.0.1:8000
or by browsing to the ``docs/_build/html`` directory.

You can also generate the documentation in formats other than HTML. Consult the
Sphinx_ documentation for more details.

.. _`reStructured Text`: http://docutils.sourceforge.net/rst.html
.. _Sphinx: http://sphinx.pocoo.org


Installable package
-------------------

Source file package
~~~~~~~~~~~~~~~~~~~

This is the sequence of step used to produce an installable package:

1. Make sure there are no lingering packages from previous attempts::

    rm dist -R

2. Generate the packaged version (will produce dist/mayan-edms-x.y.z.tar.gz)::

    python setup.py sdist

3. Do a test install::

    cd /tmp
    virtualenv venv
    source venv/bin/activate
    pip install <path of the Git repository>/dist/mayan-edms-x.y.z.tar.gz
    mayan-edms.py initialsetup
    mayan-edms.py runserver


Wheel package
~~~~~~~~~~~~~

1. Install the development requirements::

    $ pip install -r requirements/development.txt

2. Create wheel package using the source file package (Until issue #99 of wheel is fixed: https://bitbucket.org/pypa/wheel/issue/99/cannot-exclude-directory)::

    $ pip wheel --no-index --no-deps --wheel-dir dist dist/mayan-edms-x.y.z.tar.gz

3. Do a test install::

    $ cd /tmp
    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install <path of the Git repository>/dist/mayan_edms-x.y.z-py2-none-any.whl
    $ mayan-edms.py initialsetup
    $ mayan-edms.py runserver

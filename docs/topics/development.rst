.. _development:

Development
===========

**Mayan EDMS** is under active development, and contributions are welcome.

If you have a feature request, suggestion or bug report, please open a new
issue on the `GitHub issue tracker`_. To submit patches, please send a pull
request on GitHub_. Make sure to add yourself to the :ref:`contributors` file.

.. _GitHub: https://github.com/mayan-edms/mayan-edms/
.. _`GitHub issue tracker`: https://github.com/mayan-edms/mayan-edms/issues


Project philosophies
--------------------

How to think about **Mayan EDMS** when doing changes or adding new features, why things are the way they are in **Mayan EDMS**.

- Functionality must be as market/sector independent as possible, code for the 95% of use cases.
- Each user must be able to configure and customize it to their needs after install.
- Abstract as much as possible, each app must be an expert in just one thing, for other things they should use the API/classes/functions of other apps.
- Assume as little as possible about anything outside the project (hardware, OS, storage).
- Provide Python based abstraction so that a default install runs with a single step.
- No hard dependencies on binaries unless there is no other choice.
- Provide “drivers” or switchable backends to allow users to fine tune the installation.
- Call to binaries only when there is no other choice or the Python choices are not viable/mature/efficient.
- Each app is as independent and self contained as possible. Exceptions, the basic requirements: navigation, permissions, common, main.
- If an app is meant to be used by more than one other app it should be as generic as possible in regard to the project and another app will bridge the functionality.

  - Example: the acls app is app agnostic, document_acls connects the acls app with the documents app.
  - Example: since indexing (document_indexing) only applies to documents, the app is specialized and dependant on the documents app.


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

All local app module imports are in relative form, local app module name is to be referenced as little as possible, unless required by a specific feature, trick, restriction, ie: Runtime modification of the module's attributes.

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
**Mayan EDMS** apps follow a hierarchical model of dependency. Apps import from their parents or siblings, never from their children. Think plugins. A parent app must never assume anything about a possible existing child app. The documents app and the Document model are the basic entities they must never import anything else. The common and main apps are the base apps.


Variables
~~~~~~~~~
Naming of variables should follow a Major to Minor convention, usually including the purpose of the variable as the first piece of the name, using underscores as spaces. camelCase is not used in **Mayan EDMS**.

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
Quotation character used in **Mayan EDMS** for strings is the single quote. Double quote is used for multiline comments or HTML markup.


General
~~~~~~~

Code should appear in their modules in alphabetic order or in their order of importance if it makes more sense for the specific application.
This makes visual scanning easier on modules with a large number of imports, views or classes.
Class methods that return a value should be prepended with a ``get_`` to differentiate from an object’s properties.
When a variable refers to a file it should be named as follows:

- filename:  The file’s name and extension only.
- filepath:  The entire path to the file including the filename.
- path:  A path to a directory.

Flash messages should end with a period as applicable for the language.
Only exception is when the tail of the message contains an exceptions message as passed directly from the exception object.

App anatomy
~~~~~~~~~~~

- __init__.py

  - Generic initialization code (should be empty if possible)

- api.py

  - File to hold functions that are meant to be used by external apps.
  - Interfaces meant to be used by other apps that are not models or classes.

- classes.py

  - Hold python classes to be used internally or externally.
  - Any class defined by the app that is not a model.

- diagnostics.py

  - Define functions that will return the state of the data of an app.
  - Does not fixes the problems only finds them.

- events.py

  - Define history type events

- exceptions.py

  - Exceptions defined by the app

- icons.py

  - Defines the icons to be used by the links and views of the app.
  - Imports from the icons app only.

- links.py

  - Defines the links to be used by the app.
  - Import only from the navigation app and the local icons.py file.

- literals.py

  - Stores magic numbers, module choices (if static), settings defaults, and constants.
  - Should contain all capital case variables.
  - Must not import from any other module.

- maintenance.py

  - Hold functions that the user may run periodically to fix errors in the app’s data.

- permissions.py

  - Defines the permissions to be used by links and views to validate access.
  - Imports only from permissions app.
  - Link or view conditions such as testing for staff or super admin status are defined in the same file.

- statistics.py

  - Provides functions that will computer any sort of statistical information on the app’s data.

- tasks.py

  - Code to be execute as in the background or a as an process-of-process action.

- utils.py

  - Hold utilitarian code that doesn't fit on any other app file or that is used by several files in the app.
  - Anything used internally by the app that is not a class or a literal (should be as little as possible)

Views behavior
~~~~~~~~~~~~~~

- Delete views:

  - Redirect to object list view if one object is deleted.
  - Redirect to previous view if many are deleted.
  - Previous view equals:

    - previous variable in POST or
    - previous variable in GET or
    - request.META.HTTP_REFERER or
    - object list view or
    - 'home' view
    - fallback to ‘/’
    - if previous equal same view then previous should equal object list view or ‘/’


Source Control
--------------

**Mayan EDMS** source is controlled with Git_.

The project is publicly accessible, hosted and can be cloned from **GitHub** using::

    $ git clone git://github.com/mayan-edms/mayan-edms.git


Git branch structure
--------------------

**Mayan EDMS** follows the model layout by Vincent Driessen in his `Successful Git Branching Model`_ blog post. Git-flow_ is a great tool for managing the repository in this way.

``develop``
    The "next release" branch, likely unstable.
``master``
    Current production release (|version|).
``feature/``
    Unfinished/unmerged feature.
``series/``
    Released versions.


Each release is tagged and available for download on the Downloads_ section of the **Mayan EDMS** repository on GitHub_.

When submitting patches, please place your code in its own ``feature/`` branch prior to opening a pull request on GitHub_.

.. _Git: http://git-scm.org
.. _`Successful Git Branching Model`: http://nvie.com/posts/a-successful-git-branching-model/
.. _git-flow: https://github.com/nvie/gitflow
.. _Downloads:  https://github.com/mayan-edms/mayan-edms/archives/master


Steps to deploy a development version
-------------------------------------
.. code-block:: bash

    $ git clone https://github.com/mayan-edms/mayan-edms.git
    $ cd mayan-edms
    $ git checkout development
    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
    $ ./manage.py initialsetup
    $ ./manage.py runserver


Setting up a development version using Vagrant
----------------------------------------------
Make sure you have Vagrant and a provider properly installed as per https://docs.vagrantup.com/v2/installation/index.html

Start and provision a machine using:

.. code-block:: bash

    $ vagrant up

To launch a standalone development server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ vagrant ssh
    vagrant@vagrant-ubuntu-trusty-32:~$ cd ~/mayan-edms/
    vagrant@vagrant-ubuntu-trusty-32:~$ source venv/bin/activate
    vagrant@vagrant-ubuntu-trusty-32:~$ ./manage.py runserver 0.0.0.0:8000

To launch a development server with a celery worker and Redis as broker
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ vagrant ssh
    vagrant@vagrant-ubuntu-trusty-32:~$ cd ~/mayan-edms/
    vagrant@vagrant-ubuntu-trusty-32:~$ source venv/bin/activate
    vagrant@vagrant-ubuntu-trusty-32:~$ ./manage.py runserver 0.0.0.0:8000 --settings=mayan.settings.celery_redis

Then on a separate console launch a celery worker from the same provisioned Vagrant machine:

.. code-block:: bash

    $ vagrant ssh
    vagrant@vagrant-ubuntu-trusty-32:~$ cd ~/mayan-edms/
    vagrant@vagrant-ubuntu-trusty-32:~$ source venv/bin/activate
    vagrant@vagrant-ubuntu-trusty-32:~$ DJANGO_SETTINGS_MODULE='mayan.settings.celery_redis' celery -A mayan worker -l DEBUG -Q checkouts,mailing,uploads,converter,ocr,tools,indexing,metadata -Ofair -B


Contributing changes
--------------------
Once your have created and committed some new code or feature, submit a Pull Request.
Be sure to merge with mayan-edms/development before doing a pull request so that patches
apply as cleanly as possible.  If there are no conflicts, Pull Requests can be merged
directly from Github otherwise a manual command line merge has to be done and
your patches might take longer to get merged.

For more information on how to create Pull Request read: https://help.github.com/articles/using-pull-requests
or the quick version: https://help.github.com/articles/creating-a-pull-request


Debugging
---------

**Mayan EDMS** makes extensive use of Django's new `logging capabilities`_.
To enable debug logging for the ``documents`` app for example add the following
lines to your ``settings_local.py`` file::

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

**Mayan EDMS**'s documentation is written in `reStructured Text`_ format.

The documentation lives in the ``docs`` directory.  In order to build it, you will first need to install Sphinx_. ::

    $ pip install sphinx


Then, to build an HTML version of the documentation, simply run the following from the **docs** directory::

    $ make html

Your ``docs/_build/html`` directory will then contain an HTML version of the documentation, ready for publication on most web servers.

You can also generate the documentation in formats other than HTML.

.. _`reStructured Text`: http://docutils.sourceforge.net/rst.html
.. _Sphinx: http://sphinx.pocoo.org


Translations
------------

Translations are handled online via the **Transifex** website: https://www.transifex.com/projects/p/mayan-edms/.
To create a translation team for a new language or contribute to an already
existing language translation, create a **Transifex** account and contact
the team coordinator of the respective language in which you are interested.


Installable package
-------------------

Source file package
~~~~~~~~~~~~~~~~~~~

This is the sequence of step I use to produce an installable package:

1. Make sure there are no lingering packages from previous attempts::

    $ rm dist -R

2. Generate the packaged version (will produce dist/mayan-edms-1.1.0.tar.gz)::

    $ python setup.py sdist

3. Do a test install::

    $ cd /tmp
    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install <path of the Git repository>/dist/mayan-edms-1.1.0.tar.gz
    $ mayan-edms.py initialsetup
    $ mayan-edms.py runserver


Wheel package
~~~~~~~~~~~~~

1. Install wheel::

    $ pip install wheel

2. Create wheel package using the source file package (Until issue #99 of wheel is fixed: https://bitbucket.org/pypa/wheel/issue/99/cannot-exclude-directory)::

    $ pip wheel --no-index --no-deps --wheel-dir dist dist/mayan-edms-1.1.0.tar.gz

3. Do a test install::

    $ cd /tmp
    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install <path of the Git repository>/dist/mayan_edms-1.1.0-py2-none-any.whl
    $ mayan-edms.py initialsetup
    $ mayan-edms.py runserver

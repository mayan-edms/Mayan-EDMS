***********
Development
***********

Mayan EDMS is under active development, and contributions are welcome.

If you have a feature request, suggestion or bug report, please open a new
issue on the `GitLab issue tracker`_. To submit patches, please send a merge
request on GitLab_.

.. _GitLab: https://gitlab.com/mayan-edms/mayan-edms/
.. _`GitLab issue tracker`: https://gitlab.com/mayan-edms/mayan-edms/issues


Project philosophies
====================

How to think about Mayan EDMS when doing changes or adding new features;
why things are the way they are in Mayan EDMS:

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
- If an app is meant to be used by more than one other app, it should be as
  generic as possible in regard to the project and another app will bridge the functionality.

  - Example: since indexing (document_indexing) only applies to documents, the
    app is specialized and depends on the documents app.


Coding conventions
==================

Follow PEP8
-----------

Whenever possible, but don't obsess over things like line length:

.. code-block:: bash

    $ flake8 --ignore=E501,E128,E122 |less

To perform automatic PEP8 checks, install flake8's git hook using:

.. code-block:: bash

    $ flake8 --install-hook git


Imports
-------

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

All local app module imports are in relative form. Local app module name is to
be referenced as little as possible, unless required by a specific feature,
trick, restriction (e.g., Runtime modification of the module's attributes).

Incorrect:

.. code-block:: bash


    # documents app views.py model
    from documents.models import Document

Correct:

.. code-block:: bash

    # documents app views.py model
    from .models import Document


Dependencies
------------

Mayan EDMS apps follow a hierarchical model of dependency. Apps import from
their parents or siblings, never from their children. Think plugins. A parent
app must never assume anything about a possible existing child app. The
documents app and the Document model are the basic entities; they must never
import anything else. The common and main apps are the base apps.


Variables
---------

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
-------

Quotation character used in Mayan EDMS for strings is the single quote.
Double quote is used for multiple line comments or HTML markup.


Migrations
----------

Migrations should do only one thing (example: either create a table, move data
to a new table or remove an old table) to aid retrying on failure.


General
-------

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
==============

Mayan EDMS source is controlled with Git_.

The project is publicly accessible, hosted and can be cloned from **GitLab** using::

    $ git clone https://gitlab.com/mayan-edms/mayan-edms.git


Git branch structure
--------------------

Mayan EDMS follows a simplified model layout based on Vincent Driessen's
`Successful Git Branching Model`_ blog post.

``/versions/micro``
    Working branch for the next bugfix release. Micro increment (third digit).
    Only bug fixes, minor features, back-ported urgent features. This
    branch is stable and safe for production.
``/versions/minor``
    Working branch for the next minor release (second digit). New features,
    occasional breakage. Not for production but should run in test
    environment most of the time. This is the branch you will want to
    try out if you want to check out new features.
``/versions/major``
    Working branch for the next major release (first digit). New features,
    incompatible changes to the user facing interfaces. Broken most of the
    time, not for production and should only be cloned by developers
    with experience with Mayan's development.
``master``
    Current production release (|version|). Points to the latest version of
    the latest series. Production quality code.
``features/``
    Working branches for unfinished and unmerged feature. Likely unstable,
    don't use in production. Once the feature is complete, it is merged
    into one of the versions branches and deleted.
    
Special branches:

``releases/all``
    Pushing code to this branch will trigger the build and release
    a new Docker image, Documentation and Python package.
``releases/docker``
    Pushing code to this branch will trigger the build and release
    of a new Docker image to Docker Hub.
``releases/documentation``
    Pushing code to this branch will trigger the build and release
    of new documentation.
``releases/python``
    Pushing code to this branch will trigger the build and release
    of a new Python package to PyPI.
``nightly``
    Pushing code to this branch will trigger the build and release
    of a new Docker image based on development code to the GitLab image
    repository only. The image will not be published to Docker Hub.

Each release is tagged separately using annotated Git tags.

When submitting patches, please place your code in its own ``feature/`` branch
prior to opening a Merge Request on GitLab_.

.. _Git: http://git-scm.org
.. _`Successful Git Branching Model`: http://nvie.com/posts/a-successful-git-branching-model/


Commit messages
---------------

#. Use English as the language for the commit messages.
#. Provide a subject line composed of a tag and a short explanation::

    Indexing: Add document base property reindex

#. Keep the subject line to 50 or less characters.
#. Capitalize the subject line.
#. Don't end the subject line with a period, leave like a phrase in English.
#. Use active voice in the. Say what the commit will do when applied not what
   you did::

       Add new properties to the model.

   Vs.
   ::

       Added new properties to the model.

#. Limit the body of the commit to 72 characters.
#. When a commit fixes or improves an issue add the issue number in the commit
   message. Either in the subject or in the body.
#. Sign commit messages.
#. Use explicit language even for minor commits. Don't do::

       Fix typo

   Use::

       Document: Fix typo in label description


Steps to deploy a development version
=====================================

.. code-block:: bash

    $ git clone https://gitlab.com/mayan-edms/mayan-edms.git
    $ cd mayan-edms
    $ git checkout development
    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
    $ ./manage.py initialsetup
    $ ./manage.py runserver


Contributing changes
====================
Follow the latest contributing guidelines outlined here: https://gitlab.com/mayan-edms/mayan-edms/blob/master/CONTRIBUTING.md


Debugging
=========

Mayan EDMS makes extensive use of Django's new
:django-docs:`logging capabilities <topics/logging>`.

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


Documentation
=============

The documentation is written in `reStructured Text`_ format, processed with
Sphinx_, and resides in the ``docs`` directory. In order to build it, you will
first need to install the documentation editing dependencies with::

    $ pip install -r requirements/documentation.txt

Then, to build an HTML version of the documentation, run the following command
from the **docs** directory::

    $ make docs-serve

The generated documentation can be viewed by browsing to http://127.0.0.1:8000
or by browsing to the ``docs/_build/html`` directory.

You can also generate the documentation in formats other than HTML. Consult the
Sphinx_ documentation for more details.

.. _`reStructured Text`: http://docutils.sourceforge.net/rst.html
.. _Sphinx: http://sphinx.pocoo.org


Installable package
===================

Source file package
-------------------

This is the sequence of step used to produce an installable package:

1. Generate the packaged version (will produce dist/mayan-edms-x.y.z.tar.gz)::

    $ make sdist

2. Do a test install::

    $ cd /tmp
    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install <path of the Git repository>/dist/mayan-edms-x.y.z.tar.gz
    $ mayan-edms.py initialsetup
    $ mayan-edms.py runserver


Wheel package
-------------

1. Install the development requirements::

    $ pip install -r requirements/development.txt

2. Create wheel package using the makefile::

    $ make wheel

3. Do a test install::

    $ cd /tmp
    $ virtualenv venv
    $ source venv/bin/activate
    $ pip install <path of the Git repository>/dist/mayan_edms-x.y.z-py2-none-any.whl
    $ mayan-edms.py initialsetup
    $ mayan-edms.py runserver


Version numbering
=================

Mayan EDMS uses the Semantic Versioning (http://semver.org/) method to choose
version numbers along with Python's PEP-0440 (https://www.python.org/dev/peps/pep-0440/)
to format them.

X.YaN   # Alpha release
X.YbN   # Beta release
X.YrcN  # Release Candidate
X.Y     # Final release


Release checklist
=================

#. Check for missing migrations::

    make check-missing-migrations

#. Synchronize translations::

    make translations-pull

#. Compile translations::

    make translations-compile

#. Update changelog.
#. Write release notes.
#. Scan the code with flake8 for simple style warnings.
#. Check README.rst format with::

    python setup.py check -r -s

   or with::

       make check-readme

#. Bump version in ``mayan/__init__.py`` and ``docker/rootfs/version``::

    make increase-version PART=<major, minor or micro>

#. Update requirements version in ``setup.py`` using:
   ::

       make generate-setup

#. Build source package and test:
   ::

       make test-sdist-via-docker-ubuntu

#. Build wheel package and test:
   ::

       make test-wheel-via-docker-ubuntu

#. Tag version:
   ::

       git tag -a vX.Y.Z -m "Version X.Y.Z"

#. Generate set ``setup.py`` again to update the build number::

    make generate-setup

#. Commit the new ``setup.py`` file.

#. Release the version using one of the two following methods: GitLab CI or
   manual

Release using GitLab CI
-----------------------

#. Switch to the ``releases/all`` branch and merge the latest changes:
   ::

       git checkout releases/all
       git merge versions/next

#. Push code to trigger builds:
   ::

       git push

#. Push tag upstream:
   ::

       git push --tags


Manual release
--------------

#. Build and upload a test release:
   ::

       make release-test-via-docker-ubuntu

#. Build and upload a final release:
   ::

       make release-via-docker-ubuntu

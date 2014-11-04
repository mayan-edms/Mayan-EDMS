.. _development:

Development
===========

**Mayan EDMS** is under active development, and contributions are welcome.

If you have a feature request, suggestion, or bug reports, please open a new
issue on the `GitHub issue tracker`_. To submit patches, please send a pull
request on GitHub_.  Contributors are credited accordingly on the :ref:`contributors` section.

Follow the coding conventions document available at: https://github.com/mayan-edms/mayan-edms/wiki/Coding-conventions

.. _GitHub: https://github.com/mayan-edms/mayan-edms/
.. _`GitHub issue tracker`: https://github.com/mayan-edms/mayan-edms/issues


Source Control
--------------

**Mayan EDMS** source is controlled with Git_

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


Each release is tagged and available for download on the Downloads_ section of the **Mayan EDMS** repository on GitHub_

When submitting patches, please place your feature/change in its own branch prior to opening a pull request on GitHub_.

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


Contributing changes
--------------------
Once your have create and committed some new code or feature, submit a Pull Request.
Be sure to merge with mayan-edms/master before doing a pull request so that patches
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
        }
    }


Likewise, to see the debug output of the ``tags`` app, just add the following inside the ``loggers`` block::


    'tags': {
        'handlers':['console'],
        'propagate': True,
        'level':'DEBUG',
    },


.. _`logging capabilities`: https://docs.djangoproject.com/en/dev/topics/logging

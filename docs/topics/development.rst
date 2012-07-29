.. _development:

Development
===========

**Mayan EDMS** is under active development, and contributions are welcome.

If you have a feature request, suggestion, or bug reports, please open a new
issue on the `GitHub issue tracker`_. To submit patches, please send a pull request on GitHub_.  Contributors are credited accordingly on the :ref:`contributors` section.


.. _GitHub: http://github.com/rosarior/mayan/
.. _`GitHub issue tracker`: https://github.com/rosarior/mayan/issues

.. _scm:

--------------
Source Control
--------------


**Mayan EDMS** source is controlled with Git_

The project is publicly accessible, hosted and can be cloned from **GitHub** using::

    $ git clone git://github.com/rosarior/mayan.git


Git branch structure
--------------------

**Mayan EDMS** follows the model layout by Vincent Driessen in his `Successful Git Branching Model`_ blog post. Git-flow_ is a great tool for managing the repository in this way.

``develop``
    The "next release" branch, likely unstable.
``master``
    Current production release (|version|).
``feature/``
    Unfinished/ummerged feature.


Each release is tagged and available for download on the Downloads_ section of the **Mayan EDMS** repository on GitHub_

When submitting patches, please place your feature/change in its own branch prior to opening a pull request on GitHub_.
To familiarize yourself with the technical details of the project read the :ref:`internals` section.

.. _Git: http://git-scm.org
.. _`Successful Git Branching Model`: http://nvie.com/posts/a-successful-git-branching-model/
.. _git-flow: http://github.com/nvie/gitflow
.. _Downloads:  https://github.com/rosarior/mayan/archives/master

.. _docs:


---------
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


--------------------------
Automatic PDB on exception
--------------------------
For an additional tool for debugging problems in **Mayan EDMS**, set the 
configuration option ``DEBUG_ON_EXCEPTION`` to True and whenever an
exception occurs, the `Python Debugger`_ will launch automatically at
the exception point.


.. _`logging capabilities`: https://docs.djangoproject.com/en/dev/topics/logging
.. _`Python Debugger`: http://docs.python.org/library/pdb.html

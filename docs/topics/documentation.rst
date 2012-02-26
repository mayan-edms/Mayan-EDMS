=============
Documentation
=============

**Mayan EDMS**'s documentation is written in `reStructured Text`_ format.

The documentation lives in the ``docs`` directory.  In order to build it, you will first need to install Sphinx_. ::

	$ pip install sphinx


Then, to build an HTML version of the documentation, simply run the following from the **docs** directory::

	$ make html

Your ``docs/_build/html`` directory will then contain an HTML version of the documentation, ready for publication on most web servers.

You can also generate the documentation in formats other than HTML.

.. _`reStructured Text`: http://docutils.sourceforge.net/rst.html
.. _Sphinx: http://sphinx.pocoo.org

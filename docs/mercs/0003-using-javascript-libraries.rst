==================================
MERC 3: Using javascript libraries
==================================

:MERC: 3
:Author: Eric Riggs
:Status: Accepted
:Type: Feature
:Created: 2018-03-08
:Last-Modified: 2018-06-04

.. contents:: Table of Contents
   :depth: 3
   :local:


Abstract
========

This MERC proposes a standard way to use javascript libraries.

Rationale
=========

Mayan EDMS uses several javascript libraries for user interface features.
Currently, the libraries are not installed using any javascript package
manager but copied uncompressed. Installing the libraries in this manner
carries some disadvantages.

Motivation
==========

The inclusion of the libraries in source form is required by many licenses
if the library is not installed by a package manager in distributable form.
There are several disavantages with the current approach:

1. Having the library in source form means that the entire weight of the
   library's size carries over the overall size of the Mayan EDMS distribution files.
   The justification for not doing this is the same as with the Python libraries
   which are not copied with the code but downloaded upon installation.
2. Upgrading the libraries means manually examining the version of the
   installed in the project and manually searching, downloading, compressing
   and adding the files to the repository.
3. The source form of the libraries includes normal and minified versions
   of the code and the accompaning CSS files. There is no define preference
   and through the project both versions of the libraries are loaded
   interchangeably. Using a packager manager the minified version would be
   used of a pipeline to minify the installed libraries should be added.

Backwards Compatibility
=======================

There are no backwards compatibility issues with this proposal.


Specification
=============

Changes needed:

1. Python based javascript package manager. Alternatively a Python wrapper
   for a javascript package manager could be used.
2. Package manifest for the javascript libraries used.
3. Installation pipeline to install the javascript libraries during the
   installation and setup of the project.

References:

- https://github.com/JDeuce/powser
- https://github.com/javrasya/version-manager
- https://github.com/inveniosoftware-attic/setuptools-bower
- https://pypi.python.org/pypi/django-bower-cache/0.5.0
- http://django-pipeline.readthedocs.io/en/latest/index.html
- https://github.com/nvbn/django-bower

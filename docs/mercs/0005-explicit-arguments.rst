==========================
MERC 5: Explicit arguments
==========================

:MERC: 5
:Author: Roberto Rosario
:Status: Accepted
:Type: Feature
:Created: 2018-12-30
:Last-Modified: 2018-12-31

.. contents:: Table of Contents
   :depth: 3
   :local:


Abstract
========

This MERC proposes the adoption of a new methodology when performing calls.
It seeks to reduce the use of positional arguments in favor of keyword
arguments in as many places as possible.


Motivation
==========

As the project grows, legibility of code becomes more important. Keyword
argument help document the use of services, clases and functions. Refactors
that affect the interface of services are also easier to find and update and
fix. Positional argument can cause a call to continue working as long as the
datatype of the argument remains the same. Usage of keyword arguments will
automatically raise and error that will prevent such situations. Keyword
argument further eliminate the relevance of position or the arguments, and
the arguments can be sorted alphabetically for easier visual scanning or by
semantic significance improving code readability.


Specification
=============

Adoption of this MERC will require an audit of existing calls and the use
of the method proposed for new calls. Every call regardless of the type or
origin of the source callable will name each argument used. By type it is
meant: classes, functions, methods. Origin means: local from the project,
from the framework, third party libraries or the standard library.


Backwards Compatibility
=======================

No backwards compatibility issues are expected. New errors arising from the use
if keyword arguments could be interpreted as existing latent issues that
have not been uncovered.


Reference Implementation
========================

Example:

Before:

.. code-block:: python

    from mayan.apps.common.classes import Template

    Template(
        'menu_main', 'appearance/menu_main.html'
    )


After:

.. code-block:: python

    from mayan.apps.common.classes import Template

    Template(
        name='menu_main', template_name='appearance/menu_main.html'
    )


When calls use a mixture or positional and keyword arguments, the keywords
arguments can only be found after the positional arguments. Complete use
of keyword arguments allow the reposition of arguments for semantic
purposes.

Example:

Before:

.. code-block:: python

    from django.conf.urls import url

    from .views import AboutView, HomeView, RootView

    urlpatterns = [
        url(r'^$', RootView.as_view(), name='root'),
        url(r'^home/$', HomeView.as_view(), name='home'),
        url(r'^about/$', AboutView.as_view(), name='about_view'),
    ]


After:

.. code-block:: python

    from django.conf.urls import url

    from .views import AboutView, HomeView, RootView

    urlpatterns = [
        url(regex=r'^$', name='root', view=RootView.as_view()),
        url(regex=r'^home/$', name='home', view=HomeView.as_view()),
        url(regex=r'^about/$', name='about_view', view=AboutView.as_view()),
    ]


Keyword arguments should also be used for callables that pass those to others
down the line like Django's ``reverse`` function. Any change to the name of
the ``pk`` URL parameter will raise an exception in this code alerting to
any posible incompatible use.


Example:

.. code-block:: python

    def get_absolute_url(self):
        return reverse(
            viewname='documents:document_preview', kwargs={'pk': self.pk}
        )


This becomes even more important when multiple URL parameters are used. Since
the API documentation is auto generated from the code itself, it would make
sense to rename the first URL parameter from ``pk`` to ``document_pk``. Such
change will cause all address to view resolutions to break forcing their
update and allowing all consumers' interface usage to remain synchonized to the
callable's interface.

.. code-block:: python

    url(
        regex=r'^documents/(?P<pk>[0-9]+)/versions/(?P<document_version_pk>[0-9]+)/pages/(?P<document_page_pk>[0-9]+)/image/$',
        name='documentpage-image', view=APIDocumentPageImageView.as_view()
    ),

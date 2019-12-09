====================
MERC 2: Test writing
====================

:MERC: 2
:Author: Michael Price
:Status: Accepted
:Type: Feature
:Created: 2018-02-22
:Last-Modified: 2018-04-01

.. contents:: Table of Contents
   :depth: 3
   :local:

Abstract
========

This MERC proposes a standard methodology for writing tests for Mayan EDMS.

Motivation
==========

Having a standard methodology for writing tests has the following advantages:

1. Scaffolding can be reduced by providing the most frequently used
   paradigms as methods or helper functions.
2. Reduce the probabilities of errors slipping through poorly written tests.


Specification
=============

1. Tests must test each view in at least two ways:

    A. Object creations views must be tested with and without permissions.
    B. Object detail, list and delete views must be tested with and without
       object access.

2. Tests must assert the status code of the response even
   when the expected status is HTTP 200.
3. The actual request performed must be enclosed in a private methods
   so that the fail and pass tests use the same HTTP request.
4. Test must verify that changes happened and didn't happened in the
   database regardless of the return code. Even is an edit view returns
   and error 4XX (404-Not found, 403-Forbidden, etc), the test must
   ensure that the data was not indeed modified.
5. All tests must use the test user created by the BaseAPITestCase and not
   an super user unless absolutely required by the test.
6. Each test must test just one thing.
7. If a test object needs to be created before the execution of a request
   this object must be created by a private method.

Example:

.. code-block:: python

    def _request_tag_create(self):
        return self.post(
            viewname='rest_api:tag-list', data={
                'label': TEST_TAG_LABEL, 'color': TEST_TAG_COLOR
            }
        )

    def test_tag_create_view_no_permission(self):
        response = self._request_tag_create()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Tag.objects.count(), 0)

    def test_tag_create_view_with_permission(self):
        self.grant_permission(permission=permission_tag_create)
        response = self._request_tag_create()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        tag = Tag.objects.first()
        self.assertEqual(response.data['id'], tag.pk)
        self.assertEqual(response.data['label'], TEST_TAG_LABEL)
        self.assertEqual(response.data['color'], TEST_TAG_COLOR)

        self.assertEqual(Tag.objects.count(), 1)
        self.assertEqual(tag.label, TEST_TAG_LABEL)
        self.assertEqual(tag.color, TEST_TAG_COLOR)

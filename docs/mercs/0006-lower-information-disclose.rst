==================================
MERC 6: Lower information disclose
==================================

:MERC: 6
:Author: Michael Price
:Status: Accepted
:Type: Feature
:Created: 2018-12-30
:Last-Modified: 2018-12-31

.. contents:: Table of Contents
   :depth: 3
   :local:

Abstract
========

This MERC proposes the use of errors that don't disclose the existence of a
resource in the event that the requester doesn't have the required credentials.

Motivation
==========

When an user tries to perform an action like opening a view to a document for
which the required permission is missing, a permission required or access
denied error is presented. This is semantically correct, but from the stand
point of security it is still failing because it is letting the user know
that such document exists in the first place. This MERC proposes changing the
error message for existing resource to one that doesn't divulge any information
to unauthorized parties, like "Not Found".

Specification
=============

Out of the 4 basic CRUD operations, Read, Update and Delete should return an
HTTP 404 error instead of an HTTP 403 error. Only the Create operation will
continue returning the current HTTP 403 error, unless it is creating a
new resource that is related to an existing resource.

Since most view use the internal custom CRUD classes making a change to the
``ObjectPermissionCheckMixin`` class to raise an HTTP 404 on object access
failure will fulfill the proposal of this MERC.

Adding the ``object_permission_raise_404`` class attribute and setting it
to default to False will allow fulfilling the goal of this MERC while
keeping the existing functionality intact.


Example:

.. code-block:: python

    class ObjectPermissionCheckMixin(object):
        """
        If object_permission_raise_404 is True an HTTP 404 error will be raised
        instead of the normal 403.
        """
        object_permission = None
        object_permission_raise_404 = False

        def get_permission_object(self):
            return self.get_object()

        def dispatch(self, request, *args, **kwargs):
            if self.object_permission:
                try:
                    AccessControlList.objects.check_access(
                        permissions=self.object_permission, user=request.user,
                        obj=self.get_permission_object(),
                        related=getattr(self, 'object_permission_related', None)
                    )
                except PermissionDenied:
                    if self.object_permission_raise_404:
                        raise Http404
                    else:
                        raise

            return super(
                ObjectPermissionCheckMixin, self
            ).dispatch(request, *args, **kwargs)

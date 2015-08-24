===========
Permissions
===========

**Mayan EDMS** provides finegrained control over which activities users can
perform. This control is divided into two levels of operation:

2 tier permissions assignement
==============================

This level of activity control works by allowing roles that are composed
of groups or users, to be granted a permission such that the holder of that
permission can exercise it throughout the entire collection of objects
(document, folders, tags, etc). This method could be thought out as a global
permission.

3 tier access control
=====================

When more control is desired over which roles can exercise an action, this
method should be used. Under this method, roles are granted a permission but
only in relation to a selected object. Example: Granting role
``Accountants`` the ``Document view`` permission for document ``2015 Payroll report.txt``, would
allow only users in groups belonging to the ``Accountants`` role to view this document.

Inherited access control
========================

It is also possible to grant a permission to a role for a specific document type.
Under this scheme all users in groups belonging to that role will inherit that
permission for all documents of that type.

Example:

Role ``RH Supervisors`` are given the permission ``document view`` for the
document type ``Payroll reports``. Now all users in groups belonging to the
``RH Supervisors`` role can view all documents of the type ``Payroll reports``
without having to have that permissions granted for each particular Payroll report document.
If access control for the Payroll reports documents need to be updated it only needs
to be done for the document type class object and not for each document of the type
Payroll report.

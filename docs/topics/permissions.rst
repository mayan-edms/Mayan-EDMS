===========
Permissions
===========

**Mayan EDMS** provides finegrained control over which activities users can
perform. This control is divided into two levels of operation:

2 tier permissions assignement
==============================

This level of activity control works by allowing roles that are composed
of users or groups, to be granted a permission such that the holder of that
permission can exercise it throughout the entire collection of objects
(document, folders, tags, etc). This method could be thought out as a global
permission.

3 tier access control
=====================

When more control is desired over which objects actors
(user, groups and roles) can exercise an action, this method should be
used. Under this method, actors are granted a permission but only in relation
to a selected object. Example: Granting user
``Joe`` the ``Document view`` access control for document ``Payroll``, would
allow him to view this document only.

The permission system enforces inheritance by first checking, if the user
has a global permission, is a member of a group or a role that has a global
permission and if not, then checks to see if that user, a group or role to
which he belongs, has been granted access to the specific object to which
he is desiring to perform a given action.

Only when these checks fail the user is forbidden to perform the action and
a generic message is displayed to avoid providing any information
that could be used to sidetrack the permission system or obtain any kind of
information about the object to which the user was not allowed access.

Default Access Control Lists (Default ACLs)
-------------------------------------------

Default Access Control Lists allow assigment of an access control list to a
type of object (Document, Tags, Folders) before it is created. It is the default
permissions an object will have when it is created. With Default Access Control Lists
specific permissions can be granted to the creator of a document for example.

Changes to the Default Access Control Lists (Default ACLs) only affect objects
created after the change, they will not affect documents previously uploaded.

===============================
MERC XX: Unify Roles and Groups
===============================

:MERC: XX
:Author: Michael Price
:Status: Draft
:Type: Feature
:Created: 2018-02-27
:Last-Modified: 2018-02-27

.. contents:: Table of Contents
   :depth: 3
   :local:

Abstract
========

This MERC proposes the merging of the Roles and Group models.

Rationale
=========

Mayan EDMS uses Groups as units of users that are meant to mirror an
organization's actual user hierarchy. Roles are used as permission units.

Separation of concerns is a concept Mayan EDMS executes very successfully
but when it comes to the Roles/Groups relationship that execution causes
overheads without providing advantages in the day to day operations.

In reality there is almost a 1 to 1 correlation between Roles and Groups.
Other permissions systems already use Groups as permission units without
disadvantages. An example of this is LDAP and its commercial counterpart
Active Directory.

Motivation
==========

Merging the Role and Group model will reduce some complexity when initially
setting up Mayan EDMS. The merge allows removing a Mayan EDMS model in
favor of using a native Django model for the same task.

Merging the Role and Group models will also provide a speed boost in every
permission check and queryset filtering. These checks are nested in nature.
Since the access checks are performed for every view and for every link
in the view the performance gain should be substantial.

Backwards Compatibility
=======================

To avoid loss of role configuration a data migration will be needed to
convert existing roles to groups.


Specification
=============

Changes needed:

1. Data migration to convert existing roles to groups.
2. Prepend or append an identifier to the migrated roles.
3. Intermediate model to map permissions to a group. This will substitute
   the Role model's permissions many to many field.
4. Update the ``AccessControlList`` models roles field to point to the group
   models.
5. Update the role checks in the ``check_access`` and ``restrict_queryset``
   ``AccessControlList`` model manager methods.

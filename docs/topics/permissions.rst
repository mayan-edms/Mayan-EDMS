===========
Permissions
===========

Mayan EDMS provides very fine control over which actions users can
perform. Action control works by allowing ``roles``, that are composed of
``groups`` of ``users`` to be granted a ``permission`` such that the holder of
that permission can exercise it throughout the entire system.

.. blockdiag::

   blockdiag {
      orientation = portrait
      default_shape = roundedbox
      span_width = 240;
      span_height = 100;

      user [ label = 'Users' ];
      group [ label = 'Groups' ];
      role [ label = 'Roles' ];
      permission [ label = 'Permissions' ];


      user -> group -> role <- permission;
   }

In other words, users themselves can't hold a permission, permissions are
granted only to roles. Users can't directly belong to a role, they can only
belong to a group. Groups can be members of roles. Roles are system permission
units and groups are business organizational units.

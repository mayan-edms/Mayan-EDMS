from __future__ import unicode_literals


class RoleTestCaseMixin(object):
    def grant_permission(self, permission):
        self.role.permissions.add(
            permission.stored_permission
        )

from django.db import models
from django.contrib.contenttypes.models import ContentType

from permissions.runtime import permission_titles


class RoleMemberManager(models.Manager):
    def get_roles_for_member(self, member_obj):
        member_type = ContentType.objects.get_for_model(member_obj)
        return [role_member.role for role_member in self.model.objects.filter(member_type=member_type, member_id=member_obj.pk)]


class PermissionManager(models.Manager):
    def get_for_holder(self, holder):
        ct = ContentType.objects.get_for_model(holder)
        return self.model.objects.active_only().filter(permissionholder__holder_type=ct).filter(permissionholder__holder_id=holder.pk)

    def active_only(self):
        namespaces = []
        names = []
        for key in permission_titles:
            namespace, name = key.split(u'.')
            if namespace:
                namespaces.append(namespace)
            if name:
                names.append(name)
            
        return super(PermissionManager, self).get_query_set().filter(namespace__in=namespaces).filter(name__in=names).exclude(label=u'')

import logging

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError
from django.core.exceptions import ImproperlyConfigured

from common.models import AnonymousUserSingleton


logger = logging.getLogger(__name__)


class RoleMemberManager(models.Manager):
    def get_roles_for_member(self, member_obj):
        """
        Return the roles to which a member_obj belongs to.
        """
        member_obj = AnonymousUserSingleton.objects.passthru_check(member_obj)
        member_type = ContentType.objects.get_for_model(member_obj)
        return (role_member.role for role_member in self.model.objects.filter(member_type=member_type, member_id=member_obj.pk))


class StoredPermissionManager(models.Manager):
    def get_for_holder(self, holder):
        ct = ContentType.objects.get_for_model(holder)
        return self.model.objects.filter(permissionholder__holder_type=ct).filter(permissionholder__holder_id=holder.pk)

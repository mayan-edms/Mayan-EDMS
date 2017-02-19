from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.reverse import reverse

from common.serializers import ContentTypeSerializer
from permissions.serializers import PermissionSerializer, RoleSerializer

from .models import AccessControlList


class AccessControlListSerializer(serializers.ModelSerializer):
    content_type = ContentTypeSerializer(read_only=True)
    permissions_url = serializers.SerializerMethodField(
        help_text=_(
            'API URL pointing to the list of permissions for this access '
            'control list.'
        )
    )
    role = RoleSerializer(read_only=True)
    url = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'content_type', 'id', 'object_id', 'permissions_url', 'role', 'url'
        )
        model = AccessControlList

    def get_permissions_url(self, instance):
        return reverse(
            'rest_api:accesscontrollist-permission-list', args=(
                instance.content_type.app_label, instance.content_type.model,
                instance.object_id, instance.pk
            ), request=self.context['request'], format=self.context['format']
        )

    def get_url(self, instance):
        return reverse(
            'rest_api:accesscontrollist-detail', args=(
                instance.content_type.app_label, instance.content_type.model,
                instance.object_id, instance.pk
            ), request=self.context['request'], format=self.context['format']
        )


class AccessControlListPermissionSerializer(PermissionSerializer):
    acl_permission_url = serializers.SerializerMethodField(
        help_text=_(
            'API URL pointing to a permission in relation to the '
            'access control list to which it is attached. This URL is '
            'different than the canonical workflow URL.'
        )
    )

    def __init__(self, *args, **kwargs):
        super(
            AccessControlListPermissionSerializer, self
        ).__init__(*args, **kwargs)

        # Make all fields (inherited and local) read ony.
        for field in self._readable_fields:
            field.read_only = True

    def get_acl_permission_url(self, instance):
        return reverse(
            'rest_api:accesscontrollist-permission-detail', args=(
                self.context['acl'].content_type.app_label,
                self.context['acl'].content_type.model,
                self.context['acl'].object_id, self.context['acl'].pk,
                instance.stored_permission.pk
            ), request=self.context['request'], format=self.context['format']
        )

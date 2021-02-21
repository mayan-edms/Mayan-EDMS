from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from mayan.apps.common.serializers import ContentTypeSerializer
from mayan.apps.permissions import Permission
from mayan.apps.permissions.serializers import RoleSerializer
from mayan.apps.rest_api.relations import (
    FilteredPrimaryKeyRelatedField, MultiKwargHyperlinkedIdentityField
)
from mayan.apps.rest_api.serializer_mixins import CreateOnlyFieldSerializerMixin

from .models import AccessControlList


class ACLSerializer(
    CreateOnlyFieldSerializerMixin, serializers.ModelSerializer
):
    content_type = ContentTypeSerializer(read_only=True)

    permissions_add_url = MultiKwargHyperlinkedIdentityField(
        view_name='rest_api:accesscontrollist-permission-add',
        view_kwargs=(
            {
                'lookup_field': 'content_type.app_label',
                'lookup_url_kwarg': 'app_label',
            },
            {
                'lookup_field': 'content_type.model',
                'lookup_url_kwarg': 'model_name',
            },
            {
                'lookup_field': 'object_id',
                'lookup_url_kwarg': 'object_id',
            },
            {
                'lookup_field': 'pk',
                'lookup_url_kwarg': 'acl_id',
            }
        ),
    )

    permissions_remove_url = MultiKwargHyperlinkedIdentityField(
        view_name='rest_api:accesscontrollist-permission-remove',
        view_kwargs=(
            {
                'lookup_field': 'content_type.app_label',
                'lookup_url_kwarg': 'app_label',
            },
            {
                'lookup_field': 'content_type.model',
                'lookup_url_kwarg': 'model_name',
            },
            {
                'lookup_field': 'object_id',
                'lookup_url_kwarg': 'object_id',
            },
            {
                'lookup_field': 'pk',
                'lookup_url_kwarg': 'acl_id',
            }
        ),
    )

    permissions_url = MultiKwargHyperlinkedIdentityField(
        view_name='rest_api:accesscontrollist-permission-list',
        view_kwargs=(
            {
                'lookup_field': 'content_type.app_label',
                'lookup_url_kwarg': 'app_label',
            },
            {
                'lookup_field': 'content_type.model',
                'lookup_url_kwarg': 'model_name',
            },
            {
                'lookup_field': 'object_id',
                'lookup_url_kwarg': 'object_id',
            },
            {
                'lookup_field': 'pk',
                'lookup_url_kwarg': 'acl_id',
            }
        ),
    )

    role = RoleSerializer(read_only=True)
    role_id = serializers.IntegerField(write_only=True)

    url = MultiKwargHyperlinkedIdentityField(
        view_name='rest_api:accesscontrollist-detail',
        view_kwargs=(
            {
                'lookup_field': 'content_type.app_label',
                'lookup_url_kwarg': 'app_label',
            },
            {
                'lookup_field': 'content_type.model',
                'lookup_url_kwarg': 'model_name',
            },
            {
                'lookup_field': 'object_id',
                'lookup_url_kwarg': 'object_id',
            },
            {
                'lookup_field': 'pk',
                'lookup_url_kwarg': 'acl_id',
            }
        ),
    )

    class Meta:
        create_only_fields = ('role_id',)
        fields = (
            'content_type', 'id', 'object_id', 'permissions_add_url',
            'permissions_remove_url', 'permissions_url', 'role', 'role_id',
            'url'
        )
        model = AccessControlList
        read_only_fields = ('content_type', 'object_id')


class ACLPermissionAddSerializer(serializers.Serializer):
    permission = FilteredPrimaryKeyRelatedField(
        help_text=_('Primary key of the permission to add to the ACL.'),
        source_queryset=Permission.all()
    )


class ACLPermissionRemoveSerializer(serializers.Serializer):
    permission = FilteredPrimaryKeyRelatedField(
        help_text=_('Primary key of the permission to remove from the ACL.'),
        source_queryset=Permission.all()
    )

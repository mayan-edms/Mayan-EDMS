from __future__ import absolute_import, unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.reverse import reverse

from common.serializers import ContentTypeSerializer
from permissions import Permission
from permissions.models import Role
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


class WritableAccessControlListSerializer(serializers.ModelSerializer):
    permissions_pk_list = serializers.CharField(
        help_text=_(
            'Comma separated list of permission primary keys to grant to this '
            'access control list.'
        ), required=False
    )
    permissions_url = serializers.SerializerMethodField(
        help_text=_(
            'API URL pointing to the list of permissions for this access '
            'control list.'
        ), read_only=True
    )
    role_pk = serializers.IntegerField(
        help_text=_(
            'Primary keys of the role to which this access control list '
            'binds to.'
        ), required=False
    )
    url = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'content_type', 'id', 'object_id', 'permissions_pk_list',
            'permissions_url', 'role_pk', 'url'
        )
        model = AccessControlList
        read_only_fields = ('content_type', 'object_id',)

    def _add_permissions(self, instance):
        for pk in self.permissions_pk_list.split(','):
            try:
                stored_permission = Permission.get(get_dict={'pk': pk})
                instance.permissions.add(stored_permission)
                instance.save()
            except KeyError:
                raise ValidationError(_('No such permission: %s') % pk)

    def create(self, validated_data):
        validated_data['content_type'] = ContentType.objects.get_for_model(self.context['content_object'])
        validated_data['object_id'] = self.context['content_object'].pk

        self.permissions_pk_list = validated_data.pop(
            'permissions_pk_list', ''
        )

        instance = super(
            WritableAccessControlListSerializer, self
        ).create(validated_data)

        if self.permissions_pk_list:
            self._add_permissions(instance=instance)

        return instance

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

    def update(self, instance, validated_data):
        self.permissions_pk_list = validated_data.pop(
            'permissions_pk_list', ''
        )

        instance = super(WritableAccessControlListSerializer, self).update(
            instance, validated_data
        )

        if self.permissions_pk_list:
            instance.permissions.clear()
            self._add_permissions(instance=instance)

        return instance

    def validate(self, attrs):
        attrs['content_type'] = ContentType.objects.get_for_model(self.context['content_object'])
        attrs['object_id'] = self.context['content_object'].pk

        role_pk = attrs.pop('role_pk', None)
        if not role_pk:
            raise ValidationError(
                {
                    'role_pk':
                        _(
                            'This field cannot be null.'
                        )
                }
            )
        try:
            attrs['role'] = Role.objects.get(pk=role_pk)
        except Role.DoesNotExist as exception:
            raise ValidationError(force_text(exception))

        instance = AccessControlList(**attrs)
        try:
            instance.full_clean()
        except DjangoValidationError as exception:
            raise ValidationError(exception)

        return attrs

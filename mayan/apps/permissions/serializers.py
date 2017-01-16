from __future__ import unicode_literals

from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from user_management.serializers import GroupSerializer

from .classes import Permission
from .models import Role, StoredPermission


class PermissionSerializer(serializers.Serializer):
    namespace = serializers.CharField()
    pk = serializers.CharField()
    label = serializers.CharField()

    def to_representation(self, instance):
        if isinstance(instance, StoredPermission):
            return super(PermissionSerializer, self).to_representation(
                instance.volatile_permission
            )
        else:
            return super(PermissionSerializer, self).to_representation(
                instance
            )


class RoleNewGroupListSerializer(serializers.Serializer):
    group_pk_list = serializers.CharField(
        help_text=_(
            'Comma separated list of group primary keys to assign to a '
            'selected role.'
        )
    )

    def create(self, validated_data):
        validated_data['role'].groups.clear()

        try:
            pk_list = validated_data['group_pk_list'].split(',')

            for group in Group.objects.filter(pk__in=pk_list):
                validated_data['role'].groups.add(group)
        except Exception as exception:
            raise ValidationError(exception)

        return {'group_pk_list': validated_data['group_pk_list']}


class RoleNewPermissionSerializer(serializers.Serializer):
    permission_pk_list = serializers.CharField(
        help_text=_(
            'Comma separated list of permission primary keys to grant to this '
            'role.'
        )
    )

    def create(self, validated_data):
        validated_data['role'].permissions.clear()

        try:
            for pk in validated_data['permission_pk_list'].split(','):
                stored_permission = Permission.get(pk=pk)

                validated_data['role'].permissions.add(stored_permission)
        except KeyError as exception:
            raise ValidationError(_('No such permission: %s') % pk)
        except Exception as exception:
            raise ValidationError(exception)

        return {'permission_pk_list': validated_data['permission_pk_list']}


class RoleSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)
    permissions = PermissionSerializer(many=True)

    class Meta:
        fields = ('id', 'label', 'groups', 'permissions')
        model = Role

from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from mayan.apps.acls.models import AccessControlList
from mayan.apps.rest_api.mixins import ExternalObjectSerializerMixin

from .permissions import (
    permission_group_edit, permission_group_view, permission_user_edit
)
from .querysets import get_user_queryset


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    user_add_url = serializers.HyperlinkedIdentityField(
        lookup_url_kwarg='group_id', view_name='rest_api:group-user-add'
    )

    user_list_url = serializers.HyperlinkedIdentityField(
        lookup_url_kwarg='group_id', view_name='rest_api:group-user-list'
    )

    user_remove_url = serializers.HyperlinkedIdentityField(
        lookup_url_kwarg='group_id', view_name='rest_api:group-user-remove'
    )

    class Meta:
        extra_kwargs = {
            'url': {
                'lookup_url_kwarg': 'group_id',
                'view_name': 'rest_api:group-detail'
            }
        }
        fields = (
            'id', 'name', 'url', 'user_add_url', 'user_list_url',
            'user_remove_url'
        )
        model = Group


class GroupUserAddRemoveSerializer(
    ExternalObjectSerializerMixin, serializers.Serializer
):
    user_id = serializers.CharField(
        label=_('User ID'), help_text=_(
            'Primary key of the user that will be added or removed.'
        ), required=False, write_only=True
    )

    class Meta:
        external_object_queryset = get_user_queryset()
        external_object_permission = permission_user_edit
        external_object_pk_field = 'user_id'

    def users_add(self, instance):
        instance.users_add(
            queryset=self.get_external_object(as_queryset=True),
            _user=self.context['request'].user
        )

    def users_remove(self, instance):
        instance.users_remove(
            queryset=self.get_external_object(as_queryset=True),
            _user=self.context['request'].user
        )


class UserGroupListSerializer(serializers.Serializer):
    group_pk_list = serializers.CharField(
        help_text=_(
            'Comma separated list of group primary keys to assign this '
            'user to.'
        )
    )

    def create(self, validated_data):
        validated_data['user'].groups.clear()
        try:
            pk_list = validated_data['group_pk_list'].split(',')

            for group in Group.objects.filter(pk__in=pk_list):
                try:
                    AccessControlList.objects.check_access(
                        obj=group, permissions=(permission_group_view,),
                        user=self.context['request'].user
                    )
                except PermissionDenied:
                    pass
                else:
                    validated_data['user'].groups.add(group)
        except Exception as exception:
            raise ValidationError(exception)

        return {'group_pk_list': validated_data['group_pk_list']}


class UserSerializer(serializers.HyperlinkedModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)
    groups_pk_list = serializers.CharField(
        help_text=_(
            'List of group primary keys to which to add the user.'
        ), required=False
    )
    password = serializers.CharField(
        required=False, style={'input_type': 'password'}, write_only=True
    )

    class Meta:
        extra_kwargs = {
            'url': {'view_name': 'rest_api:user-detail'}
        }
        fields = (
            'first_name', 'date_joined', 'email', 'groups', 'groups_pk_list',
            'id', 'is_active', 'last_login', 'last_name', 'password', 'url',
            'username'
        )
        #TODO: block_password_change
        model = get_user_model()
        read_only_fields = ('groups', 'is_active', 'last_login', 'date_joined')
        write_only_fields = ('password', 'group_pk_list')

    def _add_groups(self, instance):
        instance.groups.add(
            *Group.objects.filter(pk__in=self.groups_pk_list.split(','))
        )

    def create(self, validated_data):
        self.groups_pk_list = validated_data.pop('groups_pk_list', '')
        password = validated_data.pop('password', None)
        instance = super(UserSerializer, self).create(validated_data)

        if password:
            instance.set_password(password)
            instance.save()

        if self.groups_pk_list:
            self._add_groups(instance=instance)

        return instance

    def update(self, instance, validated_data):
        self.groups_pk_list = validated_data.pop('groups_pk_list', '')

        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
            validated_data.pop('password')

        instance = super(UserSerializer, self).update(instance, validated_data)

        if self.groups_pk_list:
            instance.groups.clear()
            self._add_groups(instance=instance)

        return instance

    def validate(self, data):
        if 'password' in data:
            validate_password(data['password'], self.instance)

        return data

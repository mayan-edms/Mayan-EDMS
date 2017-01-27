from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    users_count = serializers.SerializerMethodField()

    class Meta:
        extra_kwargs = {
            'url': {'view_name': 'rest_api:group-detail'}
        }
        fields = ('id', 'name', 'url', 'users_count')
        model = Group

    def get_users_count(self, instance):
        return instance.user_set.count()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    groups = GroupSerializer(read_only=True, many=True)

    groups_pk_list = serializers.CharField(
        help_text=_(
            'List of group primary keys to which to the user.'
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
        model = get_user_model()
        read_only_fields = ('groups', 'is_active', 'last_login', 'date_joined')
        write_only_fields = ('password', 'group_pk_list')

    def create(self, validated_data):
        groups_pk_list = validated_data.pop('groups_pk_list', '')
        password = validated_data.pop('password', None)
        instance = super(UserSerializer, self).create(validated_data)

        if password:
            instance.set_password(password)
            instance.save()

        if groups_pk_list:
            try:
                for group in Group.objects.filter(pk__in=groups_pk_list.split(',')):
                    instance.groups.add(group)
            except Exception as exception:
                raise ValidationError(exception)

        return instance

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
            validated_data.pop('password')

        result = super(UserSerializer, self).update(instance, validated_data)

        groups_pk_list = validated_data.pop('groups_pk_list', '')

        if groups_pk_list:
            instance.groups.clear()
            try:
                for group in Group.objects.filter(pk__in=groups_pk_list.split(',')):
                    instance.groups.add(group)
            except Exception as exception:
                raise ValidationError(exception)

        return result

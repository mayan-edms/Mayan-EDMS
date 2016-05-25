from __future__ import unicode_literals

from django.contrib.auth import get_user_model

from user_management.models import MayanGroup

from rest_framework import serializers


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    users_count = serializers.SerializerMethodField()

    class Meta:
        extra_kwargs = {
            'url': {'view_name': 'rest_api:group-detail'}
        }
        fields = ('id', 'name', 'url', 'users_count')
        model = MayanGroup

    def get_users_count(self, instance):
        return instance.users.count()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    groups = GroupSerializer(many=True)

    password = serializers.CharField(
        required=False, style={'input_type': 'password'}
    )

    class Meta:
        extra_kwargs = {
            'url': {'view_name': 'rest_api:user-detail'}
        }
        fields = (
            'first_name', 'date_joined', 'email', 'groups', 'id', 'is_active',
            'last_login', 'last_name', 'url', 'username', 'password'
        )
        model = get_user_model()
        read_only_fields = ('last_login', 'date_joined')
        write_only_fields = ('password',)

    def create(self, validated_data):
        validated_data.pop('groups')
        validated_data.pop('is_active')
        user = get_user_model().on_organization.create_user(**validated_data)

        return user

    def update(self, instance, validated_data):
        validated_data.pop('groups')

        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
            validated_data.pop('password')

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance

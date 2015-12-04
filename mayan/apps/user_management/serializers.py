from __future__ import unicode_literals

from django.contrib.auth.models import Group, User

from rest_framework import serializers


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
    groups = GroupSerializer(many=True)

    class Meta:
        extra_kwargs = {
            'url': {'view_name': 'rest_api:user-detail'}
        }
        fields = (
            'first_name', 'date_joined', 'email', 'groups', 'id', 'is_staff',
            'is_active', 'is_superuser', 'last_login', 'last_name',
            'password', 'url', 'username',
        )
        model = User
        read_only_fields = ('last_login', 'date_joined')
        write_only_fields = ('password',)

    def restore_object(self, attrs, instance=None):
        user = super(UserSerializer, self).restore_object(attrs, instance)
        if 'password' in attrs:
            user.set_password(attrs['password'])
        return user

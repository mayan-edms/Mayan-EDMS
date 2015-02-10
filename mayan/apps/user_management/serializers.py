from __future__ import unicode_literals

from django.contrib.auth.models import Group, User

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined', 'password')
        model = User
        read_only_fields = ('last_login', 'date_joined')
        write_only_fields = ('password',)

    def restore_object(self, attrs, instance=None):
        user = super(UserSerializer, self).restore_object(attrs, instance)
        if 'password' in attrs:
            user.set_password(attrs['password'])
        return user


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name')
        model = Group

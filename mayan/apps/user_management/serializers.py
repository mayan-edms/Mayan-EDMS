from __future__ import absolute_import

from django.contrib.auth.models import User

from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        fields = ('id', 'url', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined')
        model = User

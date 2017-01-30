from __future__ import unicode_literals

from rest_framework import serializers

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


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'label')
        model = Role

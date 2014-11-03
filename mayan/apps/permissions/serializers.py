from rest_framework import serializers

from .models import Role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'label')
        model = Role

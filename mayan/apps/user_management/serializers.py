from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from mayan.apps.rest_api.relations import FilteredPrimaryKeyRelatedField

from .permissions import permission_user_edit
from .querysets import get_user_queryset


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    users_url = serializers.HyperlinkedIdentityField(
        help_text=_(
            'URL of the API endpoint showing the list users of this '
            'group.'
        ), lookup_url_kwarg='group_id',
        view_name='rest_api:group-user-list'
    )
    users_add_url = serializers.HyperlinkedIdentityField(
        lookup_url_kwarg='group_id',
        view_name='rest_api:group-user-add'
    )
    users_remove_url = serializers.HyperlinkedIdentityField(
        lookup_url_kwarg='group_id',
        view_name='rest_api:group-user-remove'
    )

    class Meta:
        extra_kwargs = {
            'url': {
                'lookup_url_kwarg': 'group_id',
                'view_name': 'rest_api:group-detail'
            }
        }
        fields = (
            'id', 'name', 'url', 'users_url', 'users_add_url',
            'users_remove_url'
        )
        model = Group


class GroupUserAddSerializer(serializers.Serializer):
    user = FilteredPrimaryKeyRelatedField(
        help_text=_(
            'Primary key of the user to add to the group.'
        ), source_permission=permission_user_edit,
        source_queryset=get_user_queryset()
    )


class GroupUserRemoveSerializer(serializers.Serializer):
    user = FilteredPrimaryKeyRelatedField(
        help_text=_(
            'Primary key of the user to remove from the group.'
        ), source_permission=permission_user_edit,
        source_queryset=get_user_queryset()
    )


class UserSerializer(serializers.HyperlinkedModelSerializer):
    groups_url = serializers.HyperlinkedIdentityField(
        help_text=_(
            'URL of the API endpoint showing the list groups this '
            'user belongs to.'
        ), lookup_url_kwarg='user_id',
        view_name='rest_api:user-group-list'
    )
    password = serializers.CharField(
        required=False, style={'input_type': 'password'}, write_only=True
    )

    class Meta:
        extra_kwargs = {
            'url': {
                'lookup_url_kwarg': 'user_id',
                'view_name': 'rest_api:user-detail'
            }
        }
        fields = (
            'first_name', 'date_joined', 'email', 'groups_url',
            'id', 'is_active', 'last_login', 'last_name', 'password', 'url',
            'username'
        )
        model = get_user_model()
        read_only_fields = ('is_active', 'last_login', 'date_joined')
        write_only_fields = ('password',)

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = super().create(validated_data)

        if password:
            instance._event_ignore = True
            instance.set_password(raw_password=password)
            instance.save()

        return instance

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
            validated_data.pop('password')

        instance = super().update(instance, validated_data)

        return instance

    def validate(self, data):
        if 'password' in data:
            validate_password(data['password'], self.instance)

        return data

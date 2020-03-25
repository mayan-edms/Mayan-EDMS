from django.utils.six import string_types

from actstream.models import Action
from rest_framework import serializers
from rest_framework.reverse import reverse

from mayan.apps.common.serializers import ContentTypeSerializer
from mayan.apps.rest_api.fields import DynamicSerializerField
from mayan.apps.user_management.serializers import UserSerializer

from .classes import EventType
from .models import Notification, StoredEventType


class EventTypeNamespaceSerializer(serializers.Serializer):
    label = serializers.CharField()
    name = serializers.CharField()
    url = serializers.SerializerMethodField()

    event_types_url = serializers.HyperlinkedIdentityField(
        lookup_field='name',
        view_name='rest_api:event-type-namespace-event-type-list',
    )

    def get_url(self, instance):
        return reverse(
            viewname='rest_api:event-type-namespace-detail', args=(
                instance.name,
            ), request=self.context['request'], format=self.context['format']
        )


class EventTypeSerializer(serializers.Serializer):
    label = serializers.CharField()
    name = serializers.CharField()
    id = serializers.CharField()
    event_type_namespace_url = serializers.SerializerMethodField()

    def get_event_type_namespace_url(self, instance):
        return reverse(
            viewname='rest_api:event-type-namespace-detail', args=(
                instance.namespace.name,
            ), request=self.context['request'], format=self.context['format']
        )

    def to_representation(self, instance):
        if isinstance(instance, EventType):
            return super(EventTypeSerializer, self).to_representation(
                instance
            )
        elif isinstance(instance, StoredEventType):
            return super(EventTypeSerializer, self).to_representation(
                instance.get_class()
            )
        elif isinstance(instance, string_types):
            return super(EventTypeSerializer, self).to_representation(
                EventType.get(name=instance)
            )


class EventSerializer(serializers.ModelSerializer):
    actor = DynamicSerializerField(read_only=True)
    target = DynamicSerializerField(read_only=True)
    actor_content_type = ContentTypeSerializer(read_only=True)
    target_content_type = ContentTypeSerializer(read_only=True)
    verb = EventTypeSerializer(read_only=True)

    class Meta:
        exclude = (
            'action_object_content_type', 'action_object_object_id'
        )
        model = Action


class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    action = EventSerializer(read_only=True)

    class Meta:
        fields = ('action', 'read', 'user')
        model = Notification

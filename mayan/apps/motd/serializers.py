from __future__ import absolute_import, unicode_literals

from rest_framework import serializers

from .models import Message


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        extra_kwargs = {
            'url': {
                'lookup_url_kwarg': 'message_id',
                'view_name': 'rest_api:message-detail'
            },
        }
        fields = (
            'end_datetime', 'enabled', 'label', 'message', 'start_datetime',
            'id', 'url'
        )
        model = Message

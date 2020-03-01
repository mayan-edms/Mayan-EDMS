from __future__ import unicode_literals

from rest_framework import serializers

from .models import Key


class KeySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        extra_kwargs = {
            'url': {
                'lookup_url_kwarg': 'key_id',
                'view_name': 'rest_api:key-detail'
            },
        }
        fields = (
            'algorithm', 'creation_date', 'expiration_date', 'fingerprint',
            'id', 'key_data', 'key_type', 'length', 'url', 'user_id'
        )
        model = Key

    def validate(self, attrs):
        instance = Key(**attrs)
        instance.full_clean()

        return attrs

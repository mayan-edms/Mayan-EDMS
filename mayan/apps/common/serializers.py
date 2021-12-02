from django.contrib.contenttypes.models import ContentType

from mayan.apps.rest_api import serializers


class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('app_label', 'id', 'model')
        model = ContentType
        read_only_fields = ('app_label', 'id', 'model')

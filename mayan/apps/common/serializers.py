from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers


class ContentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('app_label', 'id', 'model')
        model = ContentType

from __future__ import absolute_import

from rest_framework import serializers


class DocumentOCRSerializer(serializers.Serializer):
    document_id = serializers.IntegerField()

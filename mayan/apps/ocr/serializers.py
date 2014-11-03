from __future__ import absolute_import

from rest_framework import serializers

from .models import Document


class DocumentOCRSerializer(serializers.Serializer):
    document_id = serializers.IntegerField()

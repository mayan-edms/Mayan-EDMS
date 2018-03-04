from __future__ import unicode_literals

from rest_framework import serializers

from documents.serializers import DocumentSerializer

from .models import DocumentCheckout


class DocumentCheckoutSerializer(serializers.ModelSerializer):
    document = DocumentSerializer()

    class Meta:
        fields = ('document',)
        model = DocumentCheckout


class NewDocumentCheckoutSerializer(serializers.Serializer):
    document = serializers.IntegerField()
    expiration_datetime = serializers.DateTimeField()
    block_new_version = serializers.BooleanField()

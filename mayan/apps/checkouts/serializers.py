from __future__ import absolute_import

from rest_framework import serializers

from documents.serializers import DocumentSerializer

from .models import DocumentCheckout


#class DocumentCheckoutSerializer(serializers.Serializer):
#    document_id = serializers.IntegerField()


class DocumentCheckoutSerializer(serializers.ModelSerializer):
    document = DocumentSerializer()
    #document = serializers.IntegerField()

    class Meta:
        model = DocumentCheckout
        #fields = ('id', 'document', 'checkout_datetime', 'expiration_datetime', 'block_new_version')
        read_only_fields = ('user_content_type', 'user_object_id')


class NewDocumentCheckoutSerializer(serializers.Serializer):
    #document = DocumentSerializer()
    document = serializers.IntegerField()
    expiration_datetime = serializers.DateTimeField()
    block_new_version = serializers.BooleanField()

    #class Meta:
    #    model = DocumentCheckout
    #    fields = ('id', 'document', 'checkout_datetime', 'expiration_datetime', 'block_new_version')
    #    #read_only_fields = ('user_content_type', 'user_object_id')

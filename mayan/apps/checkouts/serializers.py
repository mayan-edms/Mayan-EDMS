from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from mayan.apps.acls.models import AccessControlList
from mayan.apps.documents.models import Document
from mayan.apps.documents.serializers.document_serializers import DocumentSerializer

from .models import DocumentCheckout
from .permissions import permission_document_check_out


class DocumentCheckoutSerializer(serializers.ModelSerializer):
    document = DocumentSerializer()

    class Meta:
        extra_kwargs = {
            'url': {
                'lookup_url_kwarg': 'checkout_id',
                'view_name': 'rest_api:checkedout-document-view'
            },
        }
        fields = ('document', 'id', 'url')
        model = DocumentCheckout


class NewDocumentCheckoutSerializer(serializers.ModelSerializer):
    block_new_file = serializers.BooleanField()
    document_pk = serializers.IntegerField(
        help_text=_('Primary key of the document to be checked out.'),
        write_only=True
    )
    expiration_datetime = serializers.DateTimeField()

    class Meta:
        fields = (
            'block_new_file', 'document', 'document_pk',
            'expiration_datetime', 'id',
        )
        model = DocumentCheckout
        read_only_fields = ('document',)
        write_only_fields = ('document_pk',)

    def create(self, validated_data):
        queryset = AccessControlList.objects.restrict_queryset(
            permission=permission_document_check_out,
            queryset=Document.valid.all(),
            user=self.context['request'].user
        )

        document = get_object_or_404(
            queryset=queryset, pk=validated_data.pop('document_pk')
        )

        validated_data['document'] = document
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data=validated_data)

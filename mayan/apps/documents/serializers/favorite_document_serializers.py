from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from mayan.apps.rest_api.serializer_mixins import CreateOnlyFieldSerializerMixin
from mayan.apps.user_management.serializers import UserSerializer

from ..models.favorite_document_models import FavoriteDocument

from .document_serializers import DocumentSerializer


class FavoriteDocumentSerializer(
    CreateOnlyFieldSerializerMixin, serializers.HyperlinkedModelSerializer
):
    document = DocumentSerializer(read_only=True)
    document_id = serializers.IntegerField(
        help_text=_('Document ID for the new favorite document.'),
        write_only=True
    )
    user = UserSerializer(read_only=True)

    class Meta:
        extra_kwargs = {
            'url': {
                'lookup_url_kwarg': 'favorite_document_id',
                'view_name': 'rest_api:favoritedocument-detail'
            },
        }
        fields = (
            'document', 'document_id', 'datetime_added', 'id', 'user', 'url'
        )
        model = FavoriteDocument
        read_only_fields = (
            'document', 'datetime_added', 'id', 'user', 'url'
        )

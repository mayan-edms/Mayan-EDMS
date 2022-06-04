from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.search import search_model_document
from mayan.apps.dynamic_search.classes import SearchModel

from .permissions import permission_signature_capture_view


#  Document

search_model_document.add_model_field(
    field='signature_captures__text', label=_('Signature capture text')
)
search_model_document.add_model_field(
    field='signature_captures__user__first_name',
    label=_('Signature capture user first name')
)
search_model_document.add_model_field(
    field='signature_captures__user__last_name',
    label=_('Signature capture user last name')
)
search_model_document.add_model_field(
    field='signature_captures__user__username',
    label=_('Signature capture user username')
)

# Signature capture

search_model_signature_capture = SearchModel(
    app_label='signature_captures', model_name='SignatureCapture',
    permission=permission_signature_capture_view,
    serializer_path='mayan.apps.signature_captures.serializers.SignatureCaptureSerializer'
)
search_model_signature_capture.add_model_field(
    field='document__document_type__label', label=_('Document type label')
)
search_model_signature_capture.add_model_field(
    field='document__label', label=_('Document label')
)
search_model_signature_capture.add_model_field(field='text')
search_model_signature_capture.add_model_field(
    field='user__first_name', label=_('User first name')
)
search_model_signature_capture.add_model_field(
    field='user__last_name', label=_('User last name')
)
search_model_signature_capture.add_model_field(
    field='user__username', label=_('User username')
)

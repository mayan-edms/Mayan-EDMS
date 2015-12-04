from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from dynamic_search.classes import SearchModel

from .permissions import permission_document_view

document_search = SearchModel(
    'documents', 'Document', permission=permission_document_view,
    serializer_string='documents.serializers.DocumentSerializer'
)

document_search.add_model_field(
    field='document_type__label', label=_('Document type')
)
document_search.add_model_field(
    field='versions__mimetype', label=_('MIME type')
)
document_search.add_model_field(field='label', label=_('Label'))
document_search.add_model_field(field='description', label=_('Description'))

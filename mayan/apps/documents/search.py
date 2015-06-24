from __future__ import absolute_import, unicode_literals

from django.utils.translation import ugettext_lazy as _

from dynamic_search.classes import SearchModel

from .permissions import PERMISSION_DOCUMENT_VIEW

document_search = SearchModel('documents', 'Document', permission=PERMISSION_DOCUMENT_VIEW, serializer_string='documents.serializers.DocumentSerializer')

document_search.add_model_field(field='document_type__name', label=_('Document type'))
document_search.add_model_field(field='versions__mimetype', label=_('MIME type'))
document_search.add_model_field(field='label', label=_('Label'))
document_search.add_model_field(field='description', label=_('Description'))

from django.db import connection
from django.utils.translation import ugettext_lazy as _
from mayan.apps.documents.search import (
    search_model_document, search_model_document_file,
    search_model_document_file_page, search_model_document_version,
    search_model_document_version_page
)
from mayan.apps.dynamic_search.classes import SearchModel

from .permissions import permission_cabinet_view


def transformation_format_uuid(term_string):
    if connection.vendor in ('mysql', 'sqlite'):
        return term_string.replace('-', '')
    else:
        return term_string


# Cabinet

search_model_cabinet = SearchModel(
    app_label='cabinets', model_name='CabinetSearchResult',
    permission=permission_cabinet_view,
    serializer_path='mayan.apps.cabinets.serializers.CabinetSerializer'
)
search_model_cabinet.add_proxy_model(
    app_label='cabinets', model_name='Cabinet'
)

search_model_cabinet.add_model_field(field='label')

# Cabinet documents

search_model_cabinet.add_model_field(
    field='documents__document_type__label', label=_('Document type')
)
search_model_cabinet.add_model_field(
    field='documents__label', label=_('Document label')
)
search_model_cabinet.add_model_field(
    field='documents__description', label=_('Document description')
)
search_model_cabinet.add_model_field(
    field='documents__uuid', label=_('Document UUID'),
    transformation_function=transformation_format_uuid
)

# Cabinet documents files

search_model_cabinet.add_model_field(
    field='documents__files__checksum', label=_('Document file checksum')
)
search_model_cabinet.add_model_field(
    field='documents__files__mimetype', label=_('Document file MIME type')
)

# Document

search_model_document.add_model_field(
    field='cabinets__label', label=_('Cabinets')
)

# Document file

search_model_document_file.add_model_field(
    field='document__cabinets__label',
    label=_('Document cabinets')
)

# Document file page

search_model_document_file_page.add_model_field(
    field='document_file__document__cabinets__label',
    label=_('Document cabinets')
)

# Document version

search_model_document_version.add_model_field(
    field='document__cabinets__label',
    label=_('Document cabinets')
)

# Document version page

search_model_document_version_page.add_model_field(
    field='document_version__document__cabinets__label',
    label=_('Document cabinets')
)

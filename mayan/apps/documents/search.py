from django.db import connection
from django.utils.translation import ugettext_lazy as _

from mayan.apps.dynamic_search.classes import SearchModel
from mayan.apps.views.literals import LIST_MODE_CHOICE_ITEM

from .permissions import (
    permission_document_file_view, permission_document_type_view,
    permission_document_version_view, permission_document_view
)


def transformation_format_uuid(term_string):
    if connection.vendor in ('mysql', 'sqlite'):
        return term_string.replace('-', '')
    else:
        return term_string


# Document

document_search = SearchModel(
    app_label='documents', default=True, label=_('Document'),
    list_mode=LIST_MODE_CHOICE_ITEM, model_name='DocumentSearchResult',
    permission=permission_document_view,
    serializer_path='mayan.apps.documents.serializers.document_serializers.DocumentSerializer'
)
document_search.add_proxy_model(app_label='documents', model_name='Document')

document_search.add_model_field(
    field='document_type__label', label=_('Document type label')
)
document_search.add_model_field(field='datetime_created')
document_search.add_model_field(field='label')
document_search.add_model_field(field='description')
document_search.add_model_field(
    field='uuid', transformation_function=transformation_format_uuid
)
document_search.add_model_field(
    field='files__checksum', label=('Document file checksum')
)
document_search.add_model_field(
    field='files__filename', label=('Document file filename')
)
document_search.add_model_field(
    field='files__mimetype', label=('Document file MIME type')
)

# Document file

document_file_search = SearchModel(
    app_label='documents', label=_('Document file'),
    list_mode=LIST_MODE_CHOICE_ITEM, model_name='DocumentFileSearchResult',
    permission=permission_document_file_view,
    serializer_path='mayan.apps.documents.serializers.document_file_serializers.DocumentFileSerializer'
)
document_file_search.add_proxy_model(
    app_label='documents', model_name='DocumentFile'
)

document_file_search.add_model_field(
    field='document__document_type__label',
    label=_('Document type label')
)
document_file_search.add_model_field(
    field='document__label', label=_('Document label')
)
document_file_search.add_model_field(
    field='document__description', label=_('Document description')
)
document_file_search.add_model_field(field='checksum')
document_file_search.add_model_field(field='comment')
document_file_search.add_model_field(field='filename')
document_file_search.add_model_field(field='mimetype')

# Document file page

document_file_page_search = SearchModel(
    app_label='documents', label=_('Document file page'),
    list_mode=LIST_MODE_CHOICE_ITEM, model_name='DocumentFilePageSearchResult',
    permission=permission_document_file_view,
    serializer_path='mayan.apps.documents.serializers.document_file_serializers.DocumentFilePageSerializer'
)
document_file_page_search.add_proxy_model(
    app_label='documents', model_name='DocumentFilePage'
)

document_file_page_search.add_model_field(
    field='document_file__document__document_type__label',
    label=_('Document type label')
)
document_file_page_search.add_model_field(
    field='document_file__document__label', label=_('Document label')
)
document_file_page_search.add_model_field(
    field='document_file__document__description',
    label=_('Document description')
)
document_file_page_search.add_model_field(
    field='document_file__checksum', label=_('Document file checksum')
)
document_file_page_search.add_model_field(
    field='document_file__mimetype', label=_('Document file MIME type')
)

# Document type

document_type_search = SearchModel(
    app_label='documents', list_mode=LIST_MODE_CHOICE_ITEM,
    model_name='DocumentType', permission=permission_document_type_view,
    serializer_path='mayan.apps.documents.serializers.document_type_serializers.DocumentTypeSerializer'
)
document_type_search.add_model_field(field='label')

# Document version

document_version_search = SearchModel(
    app_label='documents', label=_('Document version'),
    list_mode=LIST_MODE_CHOICE_ITEM, model_name='DocumentVersionSearchResult',
    permission=permission_document_version_view,
    serializer_path='mayan.apps.documents.serializers.document_version_serializers.DocumentVersionSerializer'
)
document_version_search.add_proxy_model(
    app_label='documents', model_name='DocumentVersion'
)

document_version_search.add_model_field(field='comment')
document_version_search.add_model_field(
    field='document__document_type__label',
    label=_('Document type label')
)
document_version_search.add_model_field(
    field='document__label', label=_('Document label')
)
document_version_search.add_model_field(
    field='document__description', label=_('Document description')
)

# Document version page

document_version_page_search = SearchModel(
    app_label='documents', label=_('Document version page'),
    list_mode=LIST_MODE_CHOICE_ITEM,
    model_name='DocumentVersionPageSearchResult',
    permission=permission_document_version_view,
    serializer_path='mayan.apps.documents.serializers.document_version_serializers.DocumentVersionPageSerializer'
)
document_version_page_search.add_proxy_model(
    app_label='documents', model_name='DocumentVersionPage'
)

document_version_page_search.add_model_field(
    field='document_version__document__document_type__label',
    label=_('Document type label')
)
document_version_page_search.add_model_field(
    field='document_version__comment', label=_('Document version comment')
)
document_version_page_search.add_model_field(
    field='document_version__document__label', label=_('Document label')
)
document_version_page_search.add_model_field(
    field='document_version__document__description',
    label=_('Document description')
)

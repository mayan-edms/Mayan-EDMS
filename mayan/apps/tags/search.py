from django.db import connection
from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.search import (
    search_model_document, search_model_document_file,
    search_model_document_file_page, search_model_document_version,
    search_model_document_version_page
)
from mayan.apps.dynamic_search.classes import SearchModel

from .permissions import permission_tag_view


def transformation_format_uuid(term_string):
    if connection.vendor in ('mysql', 'sqlite'):
        return term_string.replace('-', '')
    else:
        return term_string


# Document

search_model_document.add_model_field(
    field='tags__label', label=_('Tag label')
)
search_model_document.add_model_field(
    field='tags__color', label=_('Tag color')
)

# Document file

search_model_document_file.add_model_field(
    field='document__tags__label', label=_('Document tags')
)

# Document file page

search_model_document_file_page.add_model_field(
    field='document_file__document__tags__label', label=_('Document tags')
)

# Document version

search_model_document_version.add_model_field(
    field='document__tags__label', label=_('Document tags')
)

# Document version page

search_model_document_version_page.add_model_field(
    field='document_version__document__tags__label', label=_('Document tags')
)

# Tag

search_model_tag = SearchModel(
    app_label='tags', model_name='Tag',
    permission=permission_tag_view,
    serializer_path='mayan.apps.tags.serializers.TagSerializer'
)
search_model_tag.add_model_field(field='label')
search_model_tag.add_model_field(field='color')

search_model_tag.add_model_field(
    field='documents__document_type__label', label=_('Document type')
)
search_model_tag.add_model_field(
    field='documents__label', label=_('Document label')
)
search_model_tag.add_model_field(
    field='documents__description', label=_('Document description')
)
search_model_tag.add_model_field(
    field='documents__uuid', label=_('Document UUID'),
    transformation_function=transformation_format_uuid
)

search_model_tag.add_model_field(
    field='documents__files__checksum', label=_('Document file checksum')
)
search_model_tag.add_model_field(
    field='documents__files__mimetype', label=_('Document file MIME type')
)

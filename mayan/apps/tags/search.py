from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.search import (
    document_file_search, document_file_page_search, document_search,
    document_version_search, document_version_page_search
)
from mayan.apps.dynamic_search.classes import SearchModel

from .permissions import permission_tag_view

# Document

document_search.add_model_field(field='tags__label', label=_('Tags'))

# Document file

document_file_search.add_model_field(
    field='document__tags__label', label=_('Document tags')
)

# Document file page

document_file_page_search.add_model_field(
    field='document_file__document__tags__label', label=_('Document tags')
)

# Document version

document_version_search.add_model_field(
    field='document__tags__label', label=_('Document tags')
)

# Document version page

document_version_page_search.add_model_field(
    field='document_version__document__tags__label', label=_('Document tags')
)

# Tag

tag_search = SearchModel(
    app_label='tags', model_name='Tag',
    permission=permission_tag_view,
    serializer_path='mayan.apps.tags.serializers.TagSerializer'
)
tag_search.add_model_field(field='label')
tag_search.add_model_field(field='color')

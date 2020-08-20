from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.search import document_page_search, document_search
from mayan.apps.dynamic_search.classes import SearchModel

from .permissions import permission_tag_view

document_page_search.add_model_field(
    field='document_version__document__tags__label', label=_('Tags')
)
document_search.add_model_field(field='tags__label', label=_('Tags'))

tag_search = SearchModel(
    app_label='tags', model_name='Tag',
    permission=permission_tag_view,
    serializer_path='mayan.apps.tags.serializers.TagSerializer'
)
tag_search.add_model_field(field='label')
tag_search.add_model_field(field='color')

from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.search import document_page_search, document_search
from mayan.apps.dynamic_search.classes import SearchModel

from .permissions import permission_metadata_type_view

document_search.add_model_field(
    field='metadata__metadata_type__name', label=_('Metadata type')
)
document_search.add_model_field(
    field='metadata__value', label=_('Metadata value')
)

document_page_search.add_model_field(
    field='document_version__document__metadata__metadata_type__name',
    label=_('Metadata type')
)
document_page_search.add_model_field(
    field='document_version__document__metadata__value',
    label=_('Metadata value')
)

metadata_type_search = SearchModel(
    app_label='metadata', model_name='MetadataType',
    permission=permission_metadata_type_view,
    serializer_path='mayan.apps.metadata.serializers.MetadataTypeSerializer'
)

metadata_type_search.add_model_field(
    field='name', label=_('Name')
)
metadata_type_search.add_model_field(
    field='label', label=_('Label')
)
metadata_type_search.add_model_field(
    field='default', label=_('Default')
)
metadata_type_search.add_model_field(
    field='lookup', label=_('Lookup')
)
metadata_type_search.add_model_field(
    field='validation', label=_('Validator')
)
metadata_type_search.add_model_field(
    field='parser', label=_('Parser')
)

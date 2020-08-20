from django.db import connection
from django.utils.translation import ugettext_lazy as _
from mayan.apps.documents.search import document_page_search, document_search
from mayan.apps.dynamic_search.classes import SearchModel

from .permissions import permission_cabinet_view


def transformation_format_uuid(term_string):
    if connection.vendor in ('mysql', 'sqlite'):
        return term_string.replace('-', '')
    else:
        return term_string


cabinet_search = SearchModel(
    app_label='cabinets', model_name='CabinetSearchResult',
    permission=permission_cabinet_view,
    serializer_path='mayan.apps.cabinets.serializers.CabinetSerializer'
)

cabinet_search.add_model_field(field='label')

cabinet_search.add_model_field(
    field='documents__document_type__label', label=_('Document type')
)
cabinet_search.add_model_field(
    field='documents__versions__mimetype', label=_('Document MIME type')
)
cabinet_search.add_model_field(
    field='documents__label', label=_('Document label')
)
cabinet_search.add_model_field(
    field='documents__description', label=_('Document description')
)
cabinet_search.add_model_field(
    field='documents__uuid', label=_('Document UUID'),
    transformation_function=transformation_format_uuid
)
cabinet_search.add_model_field(
    field='documents__versions__checksum', label=_('Document checksum')
)

document_page_search.add_model_field(
    field='document_version__document__cabinets__label',
    label=_('Cabinets')
)
document_search.add_model_field(
    field='cabinets__label', label=_('Cabinets')
)

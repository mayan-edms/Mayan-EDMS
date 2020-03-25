from django.utils.translation import ugettext_lazy as _

from mayan.apps.dynamic_search.classes import SearchModel

from .permissions import permission_cabinet_view

cabinet_search = SearchModel(
    app_label='cabinets', model_name='Cabinet',
    permission=permission_cabinet_view,
    serializer_path='mayan.apps.cabinets.serializers.CabinetSerializer'
)

cabinet_search.add_model_field(
    field='label', label=_('Label')
)

from django.utils.translation import ugettext_lazy as _

from mayan.apps.dynamic_search.classes import SearchModel

from .permissions import permission_role_view

role_search = SearchModel(
    app_label='permissions', model_name='Role',
    permission=permission_role_view,
    serializer_path='mayan.apps.permissions.serializers.RoleSerializer'
)

role_search.add_model_field(
    field='label', label=_('Label')
)

role_search.add_model_field(
    field='groups__name', label=_('Group name')
)

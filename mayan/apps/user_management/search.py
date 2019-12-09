from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from mayan.apps.dynamic_search.classes import SearchModel

from .permissions import permission_group_view, permission_user_view
from .querysets import get_user_queryset

group_search = SearchModel(
    app_label='auth', label=_('Group'), model_name='Group',
    permission=permission_group_view,
    serializer_path='mayan.apps.user_management.serializers.GroupSerializer'
)

group_search.add_model_field(
    field='name', label=_('Name')
)

user_app, user_model = settings.AUTH_USER_MODEL.split('.')

user_search = SearchModel(
    app_label=user_app, label=_('User'), model_name=user_model,
    permission=permission_user_view, queryset=get_user_queryset,
    serializer_path='mayan.apps.user_management.serializers.UserSerializer'
)

user_search.add_model_field(
    field='first_name', label=_('First name')
)
user_search.add_model_field(
    field='email', label=_('Email')
)
user_search.add_model_field(
    field='groups__name', label=_('Groups')
)
user_search.add_model_field(
    field='last_name', label=_('Last name')
)
user_search.add_model_field(
    field='username', label=_('username')
)

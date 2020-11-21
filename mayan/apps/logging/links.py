from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link
from mayan.apps.navigation.utils import get_content_type_kwargs_factory

from .icons import icon_object_error_list, icon_object_error_list_clear
from .permissions import permission_error_log_view


link_object_error_list = Link(
    icon=icon_object_error_list,
    kwargs=get_content_type_kwargs_factory(variable_name='resolved_object'),
    permissions=(permission_error_log_view,), text=_('Errors'),
    view='logging:object_error_list',
)
link_object_error_list_clear = Link(
    icon=icon_object_error_list_clear,
    kwargs=get_content_type_kwargs_factory(variable_name='resolved_object'),
    permissions=(permission_error_log_view,), text=_('Clear errors'),
    view='logging:object_error_list_clear',
)

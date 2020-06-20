from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link
from mayan.apps.navigation.utils import get_content_type_kwargs_factory

from .permissions import permission_error_log_view


link_object_error_list = Link(
    icon_class_path='mayan.apps.logging.icons.icon_object_error_list',
    kwargs=get_content_type_kwargs_factory(variable_name='resolved_object'),
    permissions=(permission_error_log_view,), text=_('Errors'),
    view='logging:object_error_list',
)
link_object_error_list_clear = Link(
    icon_class_path='mayan.apps.logging.icons.icon_object_error_list_clear',
    kwargs=get_content_type_kwargs_factory(variable_name='resolved_object'),
    permissions=(permission_error_log_view,), text=_('Clear errors'),
    view='logging:object_error_list_clear',
)

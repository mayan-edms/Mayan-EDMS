from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

from .permissions import permission_error_log_view


def get_kwargs_factory(variable_name):
    def get_kwargs(context):
        ContentType = apps.get_model(
            app_label='contenttypes', model_name='ContentType'
        )

        content_type = ContentType.objects.get_for_model(
            model=context[variable_name]
        )
        return {
            'app_label': '"{}"'.format(content_type.app_label),
            'model': '"{}"'.format(content_type.model),
            'object_id': '{}.pk'.format(variable_name)
        }

    return get_kwargs


link_object_error_list = Link(
    icon_class_path='mayan.apps.logging.icons.icon_object_error_list',
    kwargs=get_kwargs_factory('resolved_object'),
    permissions=(permission_error_log_view,), text=_('Errors'),
    view='logging:object_error_list',
)
link_object_error_list_clear = Link(
    icon_class_path='mayan.apps.logging.icons.icon_object_error_list_clear',
    kwargs=get_kwargs_factory('resolved_object'),
    permissions=(permission_error_log_view,), text=_('Clear errors'),
    view='logging:object_error_list_clear',
)

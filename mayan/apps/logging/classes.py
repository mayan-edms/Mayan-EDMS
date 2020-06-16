from django.apps import apps
from django.utils.functional import cached_property

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.common.menus import menu_object
from mayan.apps.logging.links import link_object_error_list

from .permissions import permission_error_log_view


class ErrorLog:
    _registry = {}

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    def __init__(self, app_config):
        self.app_config = app_config

        self.__class__._registry[app_config.name] = self

    def __str__(self):
        return str(self.app_config.verbose_name)

    @cached_property
    def model(self):
        ErrorLogModel = apps.get_model(
            app_label='logging', model_name='ErrorLog'
        )

        model, created = ErrorLogModel.objects.get_or_create(name=self.app_config.name)
        return model

    def register_model(self, model, register_permission=False):
        error_log_instance = self

        @property
        def method_instance_logs(self):
            error_log_partition, created = error_log_instance.model.partitions.get_or_create(
                name='{}.{}'.format(model._meta.label, self.pk)
            )
            return error_log_partition.entries

        model.add_to_class(name='error_logs', value=method_instance_logs)

        menu_object.bind_links(
            links=(link_object_error_list,), sources=(model,)
        )

        if register_permission:
            ModelPermission.register(
                model=model, permissions=(permission_error_log_view,)
            )

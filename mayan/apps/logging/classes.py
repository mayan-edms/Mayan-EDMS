from django.apps import apps
from django.db.models.signals import pre_delete

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.common.menus import menu_list_facet

from .links import link_object_error_list
from .literals import DEFAULT_ERROR_LOG_PARTITION_ENTRY_LIMIT
from .permissions import permission_error_log_view


class ErrorLog:
    _registry = {}

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    def __init__(self, app_config, limit=DEFAULT_ERROR_LOG_PARTITION_ENTRY_LIMIT):
        self.app_config = app_config
        self.limit = limit

        self.__class__._registry[app_config.name] = self

    def __str__(self):
        return str(self.app_config.verbose_name)

    @property
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

            error_log_partition.entries.exclude(
                pk__in=error_log_partition.entries.order_by('-datetime')[:error_log_instance.limit].values('pk')
            ).delete()

            return error_log_partition.entries

        model.add_to_class(name='error_log', value=method_instance_logs)

        menu_list_facet.bind_links(
            links=(link_object_error_list,), sources=(model,)
        )

        if register_permission:
            ModelPermission.register(
                model=model, permissions=(permission_error_log_view,)
            )

        def handler_delete_model_entries(sender, instance, **kwargs):
            instance.error_log.all().delete()

        pre_delete.connect(
            dispatch_uid='logging_handler_delete_model_entries',
            receiver=handler_delete_model_entries,
            sender=model, weak=False
        )

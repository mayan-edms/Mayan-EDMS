import logging

from django.apps import apps
from django.db.models.signals import post_save, pre_delete

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.common.menus import menu_list_facet

from .links import link_object_error_list
from .literals import DEFAULT_ERROR_LOG_PARTITION_ENTRY_LIMIT
from .permissions import permission_error_log_view

logger = logging.getLogger(name=__name__)


class ErrorLog:
    _registry = {}

    @staticmethod
    def get_model_instance_partition_name(model_instance):
        return '{}.{}'.format(model_instance._meta.label, model_instance.pk)

    @classmethod
    def all(cls):
        return cls._registry

    @classmethod
    def get(cls, name):
        return cls._registry[name]

    def __init__(self, app_config, limit=DEFAULT_ERROR_LOG_PARTITION_ENTRY_LIMIT):
        self.app_config = app_config
        self.limit = limit

        self.__class__._registry[app_config.name] = self

    def __str__(self):
        return str(self.app_config.verbose_name)

    def register_model(self, model, register_permission=False):
        error_log_instance = self

        @property
        def method_instance_logs(self):
            error_log_partition, created = error_log_instance.stored_error_log.partitions.get_or_create(
                name=ErrorLog.get_model_instance_partition_name(
                    model_instance=self
                )
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

        def handler_model_instance_delete_partition(sender, instance, **kwargs):
            return self.stored_error_log.partitions.filter(
                name=ErrorLog.get_model_instance_partition_name(
                    model_instance=instance
                )
            ).delete()

        def handler_model_instance_create_partition(sender, instance, **kwargs):
            if kwargs['created']:
                return self.stored_error_log.partitions.create(
                    name=ErrorLog.get_model_instance_partition_name(
                        model_instance=instance
                    )
                )

        post_save.connect(
            dispatch_uid='logging_handler_model_instance_create_partition',
            receiver=handler_model_instance_create_partition,
            sender=model, weak=False
        )
        pre_delete.connect(
            dispatch_uid='logging_handler_model_instance_delete_partition',
            receiver=handler_model_instance_delete_partition,
            sender=model, weak=False
        )

    @property
    def stored_error_log(self):
        StoredErrorLog = apps.get_model(
            app_label='logging', model_name='StoredErrorLog'
        )
        try:
            stored_error_log, created = StoredErrorLog.objects.get_or_create(
                name=self.app_config.name
            )
        except StoredErrorLog.MultipleObjectsReturned:
            # Self heal previously repeated entries.
            StoredErrorLog.objects.filter(name=self.app_config.name).delete()
            stored_error_log, created = StoredErrorLog.objects.get_or_create(
                name=self.app_config.name
            )

        return stored_error_log

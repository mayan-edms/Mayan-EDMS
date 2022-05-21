from mayan.apps.common.compatibility import Iterable
from mayan.apps.common.utils import (
    ResolverPipelineModelAttribute, flatten_list
)

from .classes import SearchBackend
from .tasks import (
    task_deindex_instance, task_index_instance,
    task_index_related_instance_m2m
)


def handler_deindex_instance(sender, **kwargs):
    instance = kwargs['instance']

    task_deindex_instance.apply_async(
        kwargs={
            'app_label': instance._meta.app_label,
            'model_name': instance._meta.model_name,
            'object_id': instance.pk
        }
    )


def handler_factory_index_related_instance_delete(reverse_field_path):
    def handler_index_by_related_to_delete_instance(sender, **kwargs):
        related_instance = kwargs['instance']

        result = ResolverPipelineModelAttribute.resolve(
            attribute=reverse_field_path, obj=related_instance
        )

        entries = flatten_list(value=result)

        def call_task(instance):
            task_index_instance.apply_async(
                kwargs={
                    'app_label': instance._meta.app_label,
                    'model_name': instance._meta.model_name,
                    'object_id': instance.pk,
                    'exclude_app_label': related_instance._meta.app_label,
                    'exclude_model_name': related_instance._meta.model_name,
                    'exclude_kwargs': {'id': related_instance.pk}
                }
            )

        if isinstance(entries, Iterable):
            for instance in entries:
                call_task(instance=instance)
        else:
            call_task(instance=result)

    return handler_index_by_related_to_delete_instance


def handler_factory_index_related_instance_save(reverse_field_path):
    def handler_index_by_related_instance(sender, **kwargs):
        related_instance = kwargs['instance']

        result = ResolverPipelineModelAttribute.resolve(
            attribute=reverse_field_path, obj=related_instance
        )

        entries = flatten_list(value=result)

        def call_task(instance):
            task_index_instance.apply_async(
                kwargs={
                    'app_label': instance._meta.app_label,
                    'model_name': instance._meta.model_name,
                    'object_id': instance.pk
                }
            )

        if isinstance(entries, Iterable):
            for instance in entries:
                call_task(instance=instance)
        else:
            call_task(instance=result)

    return handler_index_by_related_instance


def handler_factory_index_related_instance_m2m(data):
    # Serialize search model field paths.
    serialized_search_model_related_paths = {}

    for key, value in data.items():
        serialized_search_model_related_paths[
            '{}.{}'.format(key._meta.app_label, key._meta.model_name)
        ] = tuple(value)

    def handler_index_related_instance_m2m(sender, **kwargs):
        action = kwargs.get('action')
        instance = kwargs['instance']
        model = kwargs.get('model')

        kwargs = {
            'action': action,
            'instance_app_label': instance._meta.app_label,
            'instance_model_name': instance._meta.model_name,
            'instance_object_id': instance.pk,
            'model_app_label': model._meta.app_label,
            'model_model_name': model._meta.model_name,
            'pk_set': tuple(kwargs['pk_set']),
            'serialized_search_model_related_paths': serialized_search_model_related_paths
        }

        task_index_related_instance_m2m.apply_async(
            kwargs=kwargs
        )

    return handler_index_related_instance_m2m


def handler_index_instance(sender, **kwargs):
    instance = kwargs['instance']

    task_index_instance.apply_async(
        kwargs={
            'app_label': instance._meta.app_label,
            'model_name': instance._meta.model_name,
            'object_id': instance.pk
        }
    )


def handler_search_backend_initialize(sender, **kwargs):
    backend = SearchBackend.get_instance()

    backend.initialize()


def handler_search_backend_upgrade(sender, **kwargs):
    backend = SearchBackend.get_instance()

    backend.upgrade()

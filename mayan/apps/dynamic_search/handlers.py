from collections import Iterable

from mayan.apps.common.utils import (
    ResolverPipelineModelAttribute, flatten_list
)

from .classes import SearchBackend
from .tasks import task_deindex_instance, task_index_instance


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
    def handler_index_related_instance_m2m(sender, **kwargs):
        action = kwargs.get('action')
        instance = kwargs['instance']
        model = kwargs.get('model')

        if action in ('post_add', 'pre_remove'):
            instance_paths = data.get(instance._meta.model, ())
            model_paths = data.get(model, ())

            if action == 'pre_remove':
                exclude_kwargs = {
                    'exclude_app_label': instance._meta.app_label,
                    'exclude_model_name': instance._meta.model_name,
                    'exclude_kwargs': {'id': instance.pk}
                }
            else:
                exclude_kwargs = {}

            for instance_path in instance_paths:
                result = ResolverPipelineModelAttribute.resolve(
                    attribute=instance_path, obj=instance
                )

                entries = flatten_list(value=result)

                for entry in entries:
                    task_kwargs = {
                        'app_label': entry._meta.app_label,
                        'model_name': entry._meta.model_name,
                        'object_id': entry.pk
                    }
                    task_kwargs.update(exclude_kwargs)

                    task_index_instance.apply_async(
                        kwargs=task_kwargs
                    )

            if action == 'pre_remove':
                exclude_kwargs = {
                    'exclude_app_label': model._meta.app_label,
                    'exclude_model_name': model._meta.model_name,
                    'exclude_kwargs': {'id__in': list(kwargs['pk_set'])}
                }
            else:
                exclude_kwargs = {}

            for model_instance in model._meta.default_manager.filter(pk__in=kwargs['pk_set']):
                for instance_path in model_paths:
                    result = ResolverPipelineModelAttribute.resolve(
                        attribute=instance_path, obj=model_instance
                    )

                    entries = flatten_list(value=result)

                    for entry in entries:
                        task_kwargs = {
                            'app_label': entry._meta.app_label,
                            'model_name': entry._meta.model_name,
                            'object_id': entry.pk
                        }
                        task_kwargs.update(exclude_kwargs)

                        task_index_instance.apply_async(
                            kwargs=task_kwargs
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

from mayan.apps.common.exceptions import ResolverPipelineError
from mayan.apps.common.utils import ResolverPipelineModelAttribute

from .classes import SearchModel
from .tasks import task_deindex_instance, task_index_instance


def handler_factory_deindex_instance(search_model):
    def handler_deindex_instance(sender, **kwargs):
        instance = kwargs['instance']

        task_deindex_instance.apply_async(
            kwargs={
                'app_label': instance._meta.app_label,
                'model_name': instance._meta.model_name,
                'object_id': instance.pk
            }
        )

    return handler_deindex_instance


def handler_index_instance_m2m(sender, **kwargs):
    instance = kwargs['instance']
    action = kwargs.get('action')

    if action in ('post_add', 'post_remove'):
        task_index_instance.apply_async(
            kwargs={
                'app_label': instance._meta.app_label,
                'model_name': instance._meta.model_name,
                'object_id': instance.pk
            }
        )


def handler_factory_index_related_instance_delete(reverse_field_path):
    def handler_index_by_related_instance(sender, **kwargs):
        related_instance = kwargs['instance']

        queryset = ResolverPipelineModelAttribute.resolve(
            attribute=reverse_field_path, obj=related_instance
        )

        entries = SearchModel.flatten_list(value=queryset)

        def call_task(instance):
            task_deindex_instance.apply_async(
                kwargs={
                    'app_label': instance._meta.app_label,
                    'model_name': instance._meta.model_name,
                    'object_id': instance.pk
                }
            )

        try:
            for instance in entries:
                call_task(instance=instance)
        except TypeError:
            call_task(instance=queryset)

    return handler_index_by_related_instance


def handler_factory_index_related_instance_save(reverse_field_path):
    def handler_index_by_related_instance(sender, **kwargs):
        related_instance = kwargs['instance']

        queryset = ResolverPipelineModelAttribute.resolve(
            attribute=reverse_field_path, obj=related_instance
        )

        entries = SearchModel.flatten_list(value=queryset)

        def call_task(instance):
            task_index_instance.apply_async(
                kwargs={
                    'app_label': instance._meta.app_label,
                    'model_name': instance._meta.model_name,
                    'object_id': instance.pk
                }
            )

        try:
            for instance in entries:
                call_task(instance=instance)
        except TypeError:
            call_task(instance=queryset)

    return handler_index_by_related_instance


def handler_index_instance(sender, **kwargs):
    instance = kwargs['instance']

    task_index_instance.apply_async(
        kwargs={
            'app_label': instance._meta.app_label,
            'model_name': instance._meta.model_name,
            'object_id': instance.pk
        }
    )


def handler_factory_index_related_instance_m2m(reverse_field_path):
    def handler_index_related_instance_m2m(sender, **kwargs):
        related_instance = kwargs['instance']
        action = kwargs.get('action')

        if action in ('post_add', 'post_remove'):
            try:
                queryset = ResolverPipelineModelAttribute.resolve(
                    attribute=reverse_field_path, obj=related_instance
                )
            except ResolverPipelineError:
                """
                Edge case where a related model that alread has a
                search setup register a wrong path.
                """
            else:
                entries = SearchModel.flatten_list(value=queryset)

                for instance in entries:
                    task_index_instance.apply_async(
                        kwargs={
                            'app_label': instance._meta.app_label,
                            'model_name': instance._meta.model_name,
                            'object_id': instance.pk
                        }
                    )

    return handler_index_related_instance_m2m

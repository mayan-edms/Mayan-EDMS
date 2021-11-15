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


def handler_factory_index_related_instance_save(reverse_field_path):
    def handler_index_by_related_instance(sender, **kwargs):
        related_instance = kwargs['instance']

        try:
            queryset = ResolverPipelineModelAttribute.resolve(
                attribute=reverse_field_path, obj=related_instance
            )
        except ResolverPipelineError:
            queryset = ResolverPipelineModelAttribute.resolve(
                attribute='{}_set'.format(reverse_field_path), obj=related_instance
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


def handler_factory_index_instance_m2m(model):
    def handler_index_instance_m2m(sender, **kwargs):
        instance = kwargs['instance']
        action = kwargs.get('action')

        if action in ('post_add', 'post_remove'):
            if model == instance._meta.model or model == kwargs['model']._meta.model:
                task_index_instance.apply_async(
                    kwargs={
                        'app_label': instance._meta.app_label,
                        'model_name': instance._meta.model_name,
                        'object_id': instance.pk
                    }
                )

                for pk in kwargs['pk_set']:
                    task_index_instance.apply_async(
                        kwargs={
                            'app_label': kwargs['model']._meta.app_label,
                            'model_name': kwargs['model']._meta.model_name,
                            'object_id': pk
                        }
                    )

    return handler_index_instance_m2m

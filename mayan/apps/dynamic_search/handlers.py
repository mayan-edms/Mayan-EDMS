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


def handler_index_instance(sender, **kwargs):
    instance = kwargs['instance']

    task_index_instance.apply_async(
        kwargs={
            'app_label': instance._meta.app_label,
            'model_name': instance._meta.model_name,
            'object_id': instance.pk
        }
    )

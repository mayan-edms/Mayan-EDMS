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

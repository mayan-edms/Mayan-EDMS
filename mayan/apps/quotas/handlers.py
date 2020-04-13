from django.apps import apps


def handler_process_quota_signal(sender, **kwargs):
    Quota = apps.get_model(app_label='quotas', model_name='Quota')

    for quota in Quota.objects.filter(enabled=True):
        backend_instance = quota.get_backend_instance()

        if backend_instance.sender == sender and backend_instance.signal.__class__ == kwargs['signal'].__class__:
            backend_instance.process(**kwargs)

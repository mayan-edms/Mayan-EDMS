from django.apps import apps


def purge_periodic_tasks():
    IntervalSchedule = apps.get_model(
        app_label='django_celery_beat', model_name='IntervalSchedule'
    )
    PeriodicTask = apps.get_model(
        app_label='django_celery_beat', model_name='PeriodicTask'
    )

    PeriodicTask.objects.all().delete()
    IntervalSchedule.objects.all().delete()

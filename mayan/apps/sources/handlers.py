from django.apps import apps
from django.utils.translation import ugettext_lazy as _


def handler_create_default_document_source(sender, **kwargs):
    from .source_backends.literals import SOURCE_UNCOMPRESS_CHOICE_ASK
    from .source_backends.web_form_backends import SourceBackendWebForm

    Source = apps.get_model(
        app_label='sources', model_name='Source'
    )

    if not Source.objects.filter(backend_path=SourceBackendWebForm.get_class_path()).count():
        Source.objects.create_backend(
            label=_('Default'),
            backend_path=SourceBackendWebForm.get_class_path(),
            backend_data={
                'uncompress': SOURCE_UNCOMPRESS_CHOICE_ASK
            }
        )


def handler_delete_interval_source_periodic_task(sender, instance, **kwargs):
    Source = apps.get_model(
        app_label='sources', model_name='Source'
    )

    for source in Source.objects.all():
        backend_instance = source.get_backend_instance()

        if backend_instance.kwargs.get('document_type') == instance:
            try:
                backend_instance.delete_periodic_task()
            except AttributeError:
                """
                The source has a document type but is not a periodic source,
                """


def handler_initialize_periodic_tasks(sender, **kwargs):
    Source = apps.get_model(
        app_label='sources', model_name='Source'
    )

    for source in Source.objects.filter(enabled=True):
        backend_instance = source.get_backend_instance()
        backend_instance.save()

from __future__ import unicode_literals

from django.apps import apps

from document_indexing.tasks import task_index_document


def launch_workflow(sender, instance, created, **kwargs):
    Workflow = apps.get_model(
        app_label='document_states', model_name='Workflow'
    )

    if created:
        Workflow.objects.launch_for(instance)


def handler_index_document(sender, **kwargs):
    task_index_document.apply_async(
        kwargs=dict(
            document_id=kwargs['instance'].workflow_instance.document.pk
        )
    )

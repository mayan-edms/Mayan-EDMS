from __future__ import unicode_literals

from django.db.models import get_model


def launch_workflow(sender, instance, created, **kwargs):
    Workflow = get_model('document_states', 'Workflow')

    if created:
        Workflow.objects.launch_for(instance)

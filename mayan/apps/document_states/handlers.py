from __future__ import unicode_literals

from .models import Workflow


def launch_workflow(sender, instance, created, **kwargs):
    if created:
        Workflow.objects.launch_for(instance)

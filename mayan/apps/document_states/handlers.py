from __future__ import unicode_literals


def launch_workflow(sender, instance, created, **kwargs):
    Workflow = sender.get_model('Workflow')

    if created:
        Workflow.objects.launch_for(instance)

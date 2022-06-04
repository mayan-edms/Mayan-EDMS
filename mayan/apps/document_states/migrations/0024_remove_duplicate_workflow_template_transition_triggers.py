from django.db import migrations
from django.db.models import Count


def code_remove_duplicates(apps, schema_editor):
    WorkflowTransitionTriggerEvent = apps.get_model(
        app_label='document_states',
        model_name='WorkflowTransitionTriggerEvent'
    )

    queryset = WorkflowTransitionTriggerEvent.objects.values(
        'transition', 'event_type'
    ).annotate(count=Count('id')).order_by().filter(count__gt=1)

    for workflow_transition_trigger_entry in queryset:
        workflow_transition_trigger_entry.pop('count')

        queryset_to_delete = WorkflowTransitionTriggerEvent.objects.filter(
            **workflow_transition_trigger_entry
        )[1:].values('id')

        # Redo query as 'limit' or 'offset' can't be used with delete.
        WorkflowTransitionTriggerEvent.objects.filter(
            id__in=queryset_to_delete
        ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('document_states', '0023_auto_20200930_0726')
    ]

    operations = [
        migrations.RunPython(
            code=code_remove_duplicates,
            reverse_code=migrations.RunPython.noop
        )
    ]

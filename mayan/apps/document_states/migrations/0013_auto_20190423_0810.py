from django.db import migrations


def operation_add_full_path(apps, schema_editor):
    WorkflowStateAction = apps.get_model(
        app_label='document_states', model_name='WorkflowStateAction'
    )

    for workflow_state_action in WorkflowStateAction.objects.using(schema_editor.connection.alias).all():
        workflow_state_action.action_path = 'mayan.apps.{}'.format(
            workflow_state_action.action_path
        )
        workflow_state_action.save()


def operation_remove_full_path(apps, schema_editor):
    WorkflowStateAction = apps.get_model(
        app_label='document_states', model_name='WorkflowStateAction'
    )

    for workflow_state_action in WorkflowStateAction.objects.using(schema_editor.connection.alias).all():
        workflow_state_action.action_path = workflow_state_action.action_path.replace(
            'mayan.apps.', ''
        )
        workflow_state_action.save()


class Migration(migrations.Migration):
    dependencies = [
        ('document_states', '0012_auto_20180823_2353'),
    ]

    operations = [
        migrations.RunPython(
            code=operation_add_full_path,
            reverse_code=operation_remove_full_path
        )
    ]

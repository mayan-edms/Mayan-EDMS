from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('events', '0008_auto_20180315_0029'),
        (
            'document_states',
            '0024_remove_duplicate_workflow_template_transition_triggers'
        )
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='workflowtransitiontriggerevent',
            unique_together={('transition', 'event_type')},
        )
    ]

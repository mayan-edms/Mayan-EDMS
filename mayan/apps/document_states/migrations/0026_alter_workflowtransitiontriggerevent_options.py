from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        (
            'document_states',
            '0025_alter_workflowtransitiontriggerevent_unique_together'
        )
    ]

    operations = [
        migrations.AlterModelOptions(
            name='workflowtransitiontriggerevent',
            options={
                'ordering': ('event_type__name',),
                'verbose_name': 'Workflow transition trigger event',
                'verbose_name_plural': 'Workflow transitions trigger events'
            }
        )
    ]

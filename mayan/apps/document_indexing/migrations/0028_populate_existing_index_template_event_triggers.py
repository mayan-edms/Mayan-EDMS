from django.db import migrations

from mayan.apps.events.classes import ModelEventType


def code_populate_index_template_event_triggers(apps, schema_editor):
    IndexTemplate = apps.get_model(
        app_label='document_indexing', model_name='IndexTemplate'
    )
    IndexTemplateEventTrigger = apps.get_model(
        app_label='document_indexing', model_name='IndexTemplateEventTrigger'
    )

    for index_template in IndexTemplate.objects.all():
        entries = []

        for key, value in ModelEventType._registry.items():
            # Since migration models are not real, using '.get_for_class'
            # does not work. Instead, directly inspect the model registry.
            if key._meta.model_name == 'document':
                for event_type in value:
                    entries.append(
                        IndexTemplateEventTrigger(
                            index_template=index_template,
                            stored_event_type_id=event_type.get_stored_event_type().pk
                        )
                    )

                IndexTemplateEventTrigger.objects.bulk_create(entries)


def code_populate_index_template_event_triggers_reverse(apps, schema_editor):
    IndexTemplateEventTrigger = apps.get_model(
        app_label='document_indexing', model_name='IndexTemplateEventTrigger'
    )
    IndexTemplateEventTrigger.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('document_indexing', '0027_indextemplateeventtrigger')
    ]

    operations = [
        migrations.RunPython(
            code=code_populate_index_template_event_triggers,
            reverse_code=code_populate_index_template_event_triggers_reverse
        )
    ]

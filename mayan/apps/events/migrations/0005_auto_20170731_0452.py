import re

from django.db import migrations


def operation_update_event_types_names(apps, schema_editor):
    Action = apps.get_model(app_label='actstream', model_name='Action')
    StoredEventType = apps.get_model(
        app_label='events', model_name='StoredEventType'
    )

    known_namespaces = {
        'documents_': 'documents.',
        'checkouts_': 'checkouts.',
        'document_comment_': 'document_comments.',
        'parsing_document_': 'document_parsing.',
        'ocr_': 'ocr.',
        'tag_': 'tags.',
    }

    pattern = re.compile('|'.join(known_namespaces.keys()))

    for event_type in StoredEventType.objects.using(alias=schema_editor.connection.alias).all():
        event_type.name = pattern.sub(
            lambda x: known_namespaces[x.group()], event_type.name
        )
        event_type.save()

    for action in Action.objects.using(alias=schema_editor.connection.alias).all():
        action.verb = pattern.sub(
            lambda x: known_namespaces[x.group()], action.verb
        )
        action.save()


def operation_revert_event_types_names(apps, schema_editor):
    Action = apps.get_model(app_label='actstream', model_name='Action')
    StoredEventType = apps.get_model(
        app_label='events', model_name='StoredEventType'
    )

    known_namespaces = {
        r'documents\.': 'documents_',
        r'checkouts\.': 'checkouts_',
        r'document_comments\.': 'document_comment_',
        r'document_parsing\.': 'parsing_document_',
        r'ocr\.': 'ocr_',
        r'tags\.': 'tag_',
    }

    pattern = re.compile('|'.join(known_namespaces.keys()))

    for event_type in StoredEventType.objects.using(alias=schema_editor.connection.alias).all():
        old_name = event_type.name
        new_name = pattern.sub(
            lambda x: known_namespaces[x.group().replace('.', '\\.')],
            event_type.name
        )
        event_type.name = new_name
        if old_name == new_name:
            event_type.delete()
        else:
            event_type.save()

    for action in Action.objects.using(alias=schema_editor.connection.alias).all():
        new_name = pattern.sub(
            lambda x: known_namespaces[x.group().replace('.', '\\.')],
            action.verb
        )
        action.verb = new_name
        action.save()


class Migration(migrations.Migration):
    dependencies = [
        ('events', '0004_auto_20170731_0423'),
        ('actstream', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            code=operation_update_event_types_names,
            reverse_code=operation_revert_event_types_names
        ),
    ]

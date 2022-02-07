import json

from django.db import migrations


SOURCE_BACKEND_MAPPING_LIST = [
    {
        'backend_path': 'mayan.apps.sources.source_backends.SourceBackendIMAPEmail',
        'model_name': 'IMAPEmail'
    },
    {
        'backend_path': 'mayan.apps.sources.source_backends.SourceBackendPOP3Email',
        'model_name': 'POP3Email'
    },
    {
        'backend_path': 'mayan.apps.sources.source_backends.SourceBackendSANEScanner',
        'model_name': 'SaneScanner'
    },
    {
        'backend_path': 'mayan.apps.staging_folders.source_backends.SourceBackendStagingFolder',
        'model_name': 'StagingFolderSource'
    },
    {
        'backend_path': 'mayan.apps.sources.source_backends.SourceBackendWebForm',
        'model_name': 'WebFormSource'
    },
    {
        'backend_path': 'mayan.apps.sources.source_backends.SourceBackendWatchFolder',
        'model_name': 'WatchFolderSource'
    },
]


def convert_source_model(apps, schema_editor, source_backend_mapping):
    Source = apps.get_model(app_label='sources', model_name='Source')
    Model = apps.get_model(app_label='sources', model_name=source_backend_mapping['model_name'])

    for source in Model.objects.using(alias=schema_editor.connection.alias).all():
        source.delete()
        Source.objects.create(
            backend_path=source_backend_mapping['backend_path'],
            backend_data=json.dumps(
                obj={key: value for key, value in source.__dict__.items() if not key.startswith('_')}
            ), label=source.label, enabled=source.enabled
        )


def operation_convert_sources(apps, schema_editor):
    for source_backend_mapping in SOURCE_BACKEND_MAPPING_LIST:
        convert_source_model(
            apps=apps, schema_editor=schema_editor,
            source_backend_mapping=source_backend_mapping
        )


class Migration(migrations.Migration):
    dependencies = [
        ('sources', '0026_auto_20201030_0253'),
    ]

    operations = [
        migrations.RunPython(
            code=operation_convert_sources,
            reverse_code=migrations.RunPython.noop
        ),
    ]

from django.db import migrations

from mayan.apps.databases.migrations import RemoveIndexConditional


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0056_auto_20200916_0959'),
    ]

    operations = [
        RemoveIndexConditional(
            model_name='documentversion',
            name='documents_documentversion_timestamp_30bada95'
        ),
        RemoveIndexConditional(
            model_name='documentversion',
            name='documents_documentversion_document_id_42757b7a'
        ),
        migrations.RenameModel(
            old_name='DocumentVersion',
            new_name='DocumentFile',
        ),
        migrations.AlterModelOptions(
            name='documentpageresult',
            options={
                'ordering': (
                    'document_file__document', 'page_number'
                ),
                'verbose_name': 'Document page',
                'verbose_name_plural': 'Document pages'
            },
        ),
        migrations.RenameField(
            model_name='documentpage',
            old_name='document_version',
            new_name='document_file',
        ),
    ]

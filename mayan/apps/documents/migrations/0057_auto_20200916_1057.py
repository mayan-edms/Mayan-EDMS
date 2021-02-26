from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0056_auto_20200916_0959'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DocumentVersion',
            new_name='DocumentFile',
        ),
        migrations.RunSQL
        (
            sql='DROP INDEX "documents_documentversion_timestamp_30bada95";',
            reverse_sql='CREATE INDEX "documents_documentversion_timestamp_30bada95" '
            'ON "documents_documentversion" ("timestamp");',
        ),
        migrations.RunSQL
        (
            sql='DROP INDEX "documents_documentversion_document_id_42757b7a";',
            reverse_sql='CREATE INDEX "documents_documentversion_document_id_42757b7a" '
            'ON "documents_documentversion" ("document_id");',
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

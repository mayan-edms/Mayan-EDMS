from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0057_auto_20200916_1057'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='documentfile',
            options={
                'ordering': ('timestamp',), 'verbose_name': 'Document file',
                'verbose_name_plural': 'Document files'
            },
        ),
        migrations.AlterField(
            model_name='documentfile',
            name='comment',
            field=models.TextField(
                blank=True, default='', help_text='An optional short text '
                'describing the document file.', verbose_name='Comment'
            ),
        ),
        migrations.AlterField(
            model_name='documentfile',
            name='document',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='files', to='documents.Document',
                verbose_name='Document'
            ),
        ),
        migrations.AlterField(
            model_name='documentfile',
            name='encoding',
            field=models.CharField(
                blank=True, editable=False, help_text='The document file '
                'file encoding. binary 7-bit, binary 8-bit, text, base64, '
                'etc.', max_length=64, null=True, verbose_name='Encoding'
            ),
        ),
        migrations.AlterField(
            model_name='documentfile',
            name='mimetype',
            field=models.CharField(
                blank=True, editable=False, help_text='The document '
                'file\'s file mimetype. MIME types are a standard way to '
                'describe the format of a file, in this case the file '
                'format of the document. Some examples: "text/plain" or '
                '"image/jpeg". ', max_length=255, null=True,
                verbose_name='MIME type'
            ),
        ),
        migrations.AlterField(
            model_name='documentfile',
            name='timestamp',
            field=models.DateTimeField(
                auto_now_add=True, db_index=True, help_text='The server '
                'date and time when the document file was processed.',
                verbose_name='Timestamp'
            ),
        ),
        migrations.AlterField(
            model_name='documentpage',
            name='document_file',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='file_pages', to='documents.DocumentFile',
                verbose_name='Document file'
            ),
        ),
    ]

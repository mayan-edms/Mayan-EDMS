from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0068_auto_20201024_1852'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DocumentFilePageResult',
        ),
        migrations.DeleteModel(
            name='DocumentVersionPageResult',
        ),
        migrations.CreateModel(
            name='DocumentFilePageSearchResult',
            fields=[
            ],
            options={
                'verbose_name': 'Document file page',
                'verbose_name_plural': 'Document file pages',
                'ordering': ('document_file__document', 'page_number'),
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('documents.documentfilepage',),
        ),
        migrations.CreateModel(
            name='DocumentFileSearchResult',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('documents.documentfile',),
        ),
        migrations.CreateModel(
            name='DocumentSearchResult',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('documents.document',),
        ),
        migrations.CreateModel(
            name='DocumentVersionPageSearchResult',
            fields=[
            ],
            options={
                'verbose_name': 'Document version page',
                'verbose_name_plural': 'Document version pages',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('documents.documentversionpage',),
        ),
        migrations.CreateModel(
            name='DocumentVersionSearchResult',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('documents.documentversion',),
        ),
        migrations.AlterField(
            model_name='document',
            name='label',
            field=models.CharField(
                blank=True, db_index=True, default='',
                help_text='A short text identifying the document. By '
                'default, will be set to the filename of the first file '
                'uploaded to the document.', max_length=255,
                verbose_name='Label'
            ),
        ),
        migrations.AlterField(
            model_name='document',
            name='language',
            field=models.CharField(
                blank=True, default='eng',
                help_text='The primary language in the document.',
                max_length=8, verbose_name='Language'
            ),
        ),
        migrations.AlterField(
            model_name='documentfile',
            name='filename',
            field=models.CharField(
                blank=True, max_length=255, verbose_name='Filename'
            ),
        ),
        migrations.AlterField(
            model_name='documentversionpage',
            name='content_type',
            field=models.ForeignKey(
                help_text='Content type for the source object of the page.',
                on_delete=django.db.models.deletion.CASCADE,
                to='contenttypes.ContentType'
            ),
        ),
        migrations.AlterField(
            model_name='documentversionpage',
            name='object_id',
            field=models.PositiveIntegerField(
                help_text='ID for the source object of the page.'
            ),
        ),
        migrations.AlterField(
            model_name='documentversionpage',
            name='page_number',
            field=models.PositiveIntegerField(
                db_index=True, default=1,
                help_text='Unique integer number for the page. Pages are '
                'ordered by this number.', verbose_name='Page number'
            ),
        ),
    ]

from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('documents', '0052_rename_document_page'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enabled', models.BooleanField(default=True, verbose_name='Enabled')),
                ('page_number', models.PositiveIntegerField(blank=True, db_index=True, null=True, verbose_name='Page number')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pages', to='documents.Document', verbose_name='Document')),
            ],
            options={
                'unique_together': set([('document', 'page_number')]),
                'verbose_name': 'Document page',
                'verbose_name_plural': 'Document pages',
                'ordering': ('page_number',),
            },
        ),
        migrations.CreateModel(
            name='DocumentPageResult',
            fields=[
            ],
            options={
                'verbose_name': 'Document page result',
                'verbose_name_plural': 'Document pages result',
                'ordering': ('document', 'page_number'),
                'proxy': True,
                'indexes': [],
            },
            bases=('documents.documentpage',),
        ),
        migrations.CreateModel(
            name='DocumentVersionPageResult',
            fields=[
            ],
            options={
                'verbose_name': 'Document version page',
                'verbose_name_plural': 'Document version pages',
                'ordering': ('document_version__document', 'page_number'),
                'proxy': True,
                'indexes': [],
            },
            bases=('documents.documentversionpage',),
        ),
    ]

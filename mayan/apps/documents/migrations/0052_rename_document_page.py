from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0051_documentpage_enabled'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DocumentPageResult',
        ),
        migrations.RenameModel('DocumentPage', 'DocumentVersionPage'),
        migrations.AlterField(
            model_name='documentversionpage',
            name='document_version',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='pages', to='documents.DocumentVersion',
                verbose_name='Document version'
            ),
        ),
        migrations.RemoveField(
            model_name='documentversionpage',
            name='enabled',
        ),
        migrations.AlterModelOptions(
            name='documentversionpage',
            options={
                'ordering': ('page_number',),
                'verbose_name': 'Document version page',
                'verbose_name_plural': 'Document version pages'
            },
        ),
    ]

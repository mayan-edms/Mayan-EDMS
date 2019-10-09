from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('document_parsing', '0004_auto_20180917_0645'),
        ('documents', '0052_rename_document_page'),
    ]

    operations = [
        migrations.RenameModel(
            'DocumentPageContent', 'DocumentVersionPageContent'
        ),
        migrations.AlterField(
            model_name='documentversionpagecontent',
            name='document_page',
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                name='document_version_page',
                related_name='content',
                to='documents.DocumentVersionPage',
                verbose_name='Document version page'
            ),
        ),
    ]

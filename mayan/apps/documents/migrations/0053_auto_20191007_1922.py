from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0052_auto_20191007_1921'),
        ('ocr', '0008_auto_20180917_0646'),
        ('document_parsing', '0004_auto_20180917_0645'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentPageResult',
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

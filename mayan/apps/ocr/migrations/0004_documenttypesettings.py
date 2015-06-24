# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0008_auto_20150624_0520'),
        ('ocr', '0003_auto_20150617_0401'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentTypeSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('auto_ocr', models.BooleanField(default=True, verbose_name='Automatically queue newly created documents for OCR.')),
                ('document_type', models.OneToOneField(related_name='ocr_settings', verbose_name='Document type', to='documents.DocumentType')),
            ],
            options={
                'verbose_name': 'Document type settings',
                'verbose_name_plural': 'Document types settings',
            },
            bases=(models.Model,),
        ),
    ]

from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0052_auto_20191130_2209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='document_type',
            field=models.ForeignKey(
                help_text='The document type of the document.',
                on_delete=django.db.models.deletion.CASCADE,
                related_name='documents', to='documents.DocumentType',
                verbose_name='Document type'
            ),
        ),
    ]

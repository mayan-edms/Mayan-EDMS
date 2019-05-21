from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('document_parsing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentversionparseerror',
            name='document_version',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='parsing_errors',
                to='documents.DocumentVersion',
                verbose_name='Document version'
            ),
        ),
    ]

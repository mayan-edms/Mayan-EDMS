from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document_parsing', '0003_documenttypesettings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentpagecontent',
            name='content',
            field=models.TextField(
                blank=True, help_text='The actual text content as extracted '
                'by the document parsing backend.', verbose_name='Content'
            ),
        ),
    ]

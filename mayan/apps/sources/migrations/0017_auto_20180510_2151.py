from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sources', '0016_auto_20170630_2040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sanescanner',
            name='source',
            field=models.CharField(
                blank=True, choices=[
                    ('flatbed', 'Flatbed'),
                    ('Automatic Document Feeder', 'Document feeder')
                ],
                help_text='Selects the scan source (such as a '
                'document-feeder). If this option is not supported by your '
                'scanner, leave it blank.', max_length=32, null=True,
                verbose_name='Paper source'
            ),
        ),
    ]

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('sources', '0014_auto_20170206_0722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sanescanner',
            name='source',
            field=models.CharField(
                blank=True, choices=[
                    ('flatbed', 'Flatbed'),
                    ('Automatic Document Feeder', 'Document feeder')
                ], default='flatbed', help_text='Selects the scan source '
                '(such as a document-feeder). If this option is not '
                'supported by your scanner, leave it blank.', max_length=32,
                verbose_name='Paper source'
            ),
        ),
    ]

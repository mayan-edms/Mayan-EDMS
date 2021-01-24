from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('duplicates', '0008_auto_20201130_0847'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='duplicatebackendentry',
            name='datetime_added',
        ),
        migrations.AlterField(
            model_name='storedduplicatebackend',
            name='backend_data',
            field=models.TextField(
                blank=True, help_text='JSON encoded data for the backend '
                'class.', verbose_name='Backend data'
            ),
        ),
    ]

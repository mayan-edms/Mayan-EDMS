from django.db import migrations, models
import django.db.models.deletion

DEFAULT_FALSE_CONTENT_TYPE_ID = 1
DEFAULT_FALSE_OBJECT_ID = 1


class Migration(migrations.Migration):
    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('logging', '0003_auto_20211201_1055')
    ]

    operations = [
        migrations.CreateModel(
            bases=('logging.errorlogpartitionentry',), fields=[],
            name='GlobalErrorLogPartitionEntry', options={
                'constraints': [],
                'indexes': [],
                'proxy': True
            }
        ),
        migrations.AddField(
            field=models.ForeignKey(
                default=DEFAULT_FALSE_CONTENT_TYPE_ID,
                on_delete=django.db.models.deletion.CASCADE,
                to='contenttypes.contenttype'
            ), model_name='errorlogpartition', name='content_type',
            preserve_default=False
        ),
        migrations.AddField(
            field=models.PositiveIntegerField(
                default=DEFAULT_FALSE_OBJECT_ID
            ), model_name='errorlogpartition', name='object_id',
            preserve_default=False
        ),
    ]

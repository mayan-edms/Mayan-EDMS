from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('file_caching', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cache',
            name='label',
            field=models.CharField(
                help_text='A short text describing the cache.',
                max_length=128, verbose_name='Label'
            ),
        ),
        migrations.AlterField(
            model_name='cache',
            name='maximum_size',
            field=models.PositiveIntegerField(
                help_text='Maximum size of the cache in bytes.',
                verbose_name='Maximum size'
            ),
        ),
        migrations.AlterField(
            model_name='cache',
            name='name',
            field=models.CharField(
                help_text='Internal name of the cache.', max_length=128,
                unique=True, verbose_name='Name'
            ),
        ),
        migrations.AlterField(
            model_name='cache',
            name='storage_instance_path',
            field=models.CharField(
                help_text='Dotted path to the actual storage class used '
                'for the cache.', max_length=255, unique=True,
                verbose_name='Storage instance path'
            ),
        ),
    ]

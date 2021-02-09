from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('file_caching', '0005_auto_20200322_0607'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cache',
            name='label',
        ),
        migrations.RemoveField(
            model_name='cache',
            name='name',
        ),
        migrations.RemoveField(
            model_name='cache',
            name='storage_instance_path',
        ),
        migrations.AddField(
            model_name='cache',
            name='defined_storage_name',
            field=models.CharField(
                db_index=True, default='', help_text='Internal name of '
                'the defined storage for this cache.', max_length=96,
                unique=True, verbose_name='Defined storage name'
            ),
            preserve_default=False,
        ),
    ]

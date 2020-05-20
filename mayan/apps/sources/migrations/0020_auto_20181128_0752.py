from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('sources', '0019_auto_20180803_0440'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchfoldersource',
            name='include_subdirectories',
            field=models.BooleanField(
                default=False, help_text='If checked, not only will the '
                'folder path be scanned for files but also its '
                'subdirectories.', verbose_name='Include subdirectories?'
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='watchfoldersource',
            name='folder_path',
            field=models.CharField(
                help_text='Server side filesystem path to scan for files.',
                max_length=255, verbose_name='Folder path'
            ),
        ),
    ]

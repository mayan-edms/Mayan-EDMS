from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('sources', '0027_auto_20201030_0259'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imapemail',
            name='emailbasemodel_ptr',
        ),
        migrations.RemoveField(
            model_name='pop3email',
            name='emailbasemodel_ptr',
        ),
        migrations.RemoveField(
            model_name='emailbasemodel',
            name='intervalbasemodel_ptr',
        ),
        migrations.RemoveField(
            model_name='sanescanner',
            name='interactivesource_ptr',
        ),
        migrations.RemoveField(
            model_name='stagingfoldersource',
            name='interactivesource_ptr',
        ),
        migrations.RemoveField(
            model_name='watchfoldersource',
            name='intervalbasemodel_ptr',
        ),
        migrations.RemoveField(
            model_name='webformsource',
            name='interactivesource_ptr',
        ),
        migrations.RemoveField(
            model_name='intervalbasemodel',
            name='document_type',
        ),
        migrations.RemoveField(
            model_name='intervalbasemodel',
            name='outofprocesssource_ptr',
        ),
        migrations.DeleteModel(
            name='EmailBaseModel',
        ),
        migrations.DeleteModel(
            name='IMAPEmail',
        ),
        migrations.DeleteModel(
            name='InteractiveSource',
        ),
        migrations.DeleteModel(
            name='IntervalBaseModel',
        ),
        migrations.DeleteModel(
            name='OutOfProcessSource',
        ),
        migrations.DeleteModel(
            name='POP3Email',
        ),
        migrations.DeleteModel(
            name='SaneScanner',
        ),
        migrations.DeleteModel(
            name='StagingFolderSource',
        ),
        migrations.DeleteModel(
            name='WatchFolderSource',
        ),
        migrations.DeleteModel(
            name='WebFormSource',
        ),
        migrations.AlterField(
            model_name='source',
            name='backend_data',
            field=models.TextField(
                blank=True, help_text='JSON encoded data for the backend '
                'class.', verbose_name='Backend data'
            ),
        ),
    ]

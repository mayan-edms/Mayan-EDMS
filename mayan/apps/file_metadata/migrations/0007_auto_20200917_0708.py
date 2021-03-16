from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('file_metadata', '0006_rename_documentversiondriverentry_model'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='documentfiledriverentry',
            options={
                'ordering': ('document_file', 'driver'),
                'verbose_name': 'Document file driver entry',
                'verbose_name_plural': 'Document file driver entries'
            },
        ),
        migrations.AlterField(
            model_name='documentfiledriverentry',
            name='document_file',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='file_metadata_drivers',
                to='documents.DocumentFile', verbose_name='Document file'
            ),
        ),
        migrations.AlterField(
            model_name='filemetadataentry',
            name='document_file_driver_entry',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='entries',
                to='file_metadata.DocumentFileDriverEntry',
                verbose_name='Document file driver entry'
            ),
        ),
    ]

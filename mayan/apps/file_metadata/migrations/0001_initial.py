from django.db import migrations, models
import django.db.models.deletion


def operation_initialize_file_metadata_settings(apps, schema_editor):
    DocumentType = apps.get_model(
        app_label='documents', model_name='DocumentType'
    )
    DocumentTypeSettings = apps.get_model(
        app_label='file_metadata', model_name='DocumentTypeSettings'
    )

    for document_type in DocumentType.objects.using(alias=schema_editor.connection.alias).all():
        DocumentTypeSettings.objects.using(
            alias=schema_editor.connection.alias
        ).create(document_type=document_type)


def operation_initialize_file_metadata_settings_reverse(apps, schema_editor):
    DocumentTypeSettings = apps.get_model(
        app_label='file_metadata', model_name='DocumentTypeSettings'
    )
    DocumentTypeSettings.objects.using(alias=schema_editor.connection.alias).delete()


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('documents', '0047_auto_20180917_0737'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentTypeSettings',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True, primary_key=True, serialize=False,
                        verbose_name='ID'
                    )
                ),
                (
                    'auto_process', models.BooleanField(
                        default=True, verbose_name='Automatically queue '
                        'newly created documents for processing.'
                    )
                ),
                (
                    'document_type', models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='file_metadata_settings',
                        to='documents.DocumentType',
                        verbose_name='Document type'
                    )
                ),
            ],
            options={
                'verbose_name': 'Document type settings',
                'verbose_name_plural': 'Document types settings',
            },
        ),
        migrations.CreateModel(
            name='DocumentVersionDriverEntry',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True, primary_key=True, serialize=False,
                        verbose_name='ID'
                    )
                ),
                (
                    'document_version', models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='file_metadata_drivers',
                        to='documents.DocumentVersion',
                        verbose_name='Document version'
                    )
                ),
            ],
            options={
                'ordering': ('document_version', 'driver'),
                'verbose_name': 'Document version driver entry',
                'verbose_name_plural': 'Document version driver entries',
            },
        ),
        migrations.CreateModel(
            name='FileMetadataEntry',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True, primary_key=True, serialize=False,
                        verbose_name='ID'
                    )
                ),
                (
                    'key', models.CharField(
                        db_index=True, help_text='Name of the file metadata '
                        'entry.', max_length=255, verbose_name='Key'
                    )
                ),
                (
                    'value', models.CharField(
                        db_index=True, help_text='Value of the file metadata '
                        'entry.', max_length=255, verbose_name='Value'
                    )
                ),
                (
                    'document_version_driver_entry', models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='entries',
                        to='file_metadata.DocumentVersionDriverEntry',
                        verbose_name='Document version driver entry'
                    )
                ),
            ],
            options={
                'ordering': ('key', 'value'),
                'verbose_name': 'File metadata entry',
                'verbose_name_plural': 'File metadata entries',
            },
        ),
        migrations.CreateModel(
            name='StoredDriver',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True, primary_key=True, serialize=False,
                        verbose_name='ID'
                    )
                ),
                (
                    'driver_path', models.CharField(
                        max_length=255, verbose_name='Driver path'
                    )
                ),
                (
                    'internal_name', models.CharField(
                        db_index=True, max_length=128,
                        verbose_name='Internal name'
                    )
                ),
            ],
            options={
                'ordering': ('internal_name',),
                'verbose_name': 'Driver',
                'verbose_name_plural': 'Drivers',
            },
        ),
        migrations.AddField(
            model_name='documentversiondriverentry',
            name='driver',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='driver_entries',
                to='file_metadata.StoredDriver', verbose_name='Driver'
            ),
        ),
        migrations.AlterUniqueTogether(
            name='documentversiondriverentry',
            unique_together=set([('driver', 'document_version')]),
        ),
        migrations.RunPython(
            code=operation_initialize_file_metadata_settings,
            reverse_code=operation_initialize_file_metadata_settings_reverse
        )
    ]

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0075_delete_duplicateddocumentold'),
        ('duplicates', '0006_duplicateddocument_stored_backend'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DuplicatedDocument',
            new_name='DuplicateBackendEntry',
        ),
        migrations.AlterModelOptions(
            name='duplicatebackendentry',
            options={
                'verbose_name': 'Duplicated backend entry',
                'verbose_name_plural': 'Duplicated backend entries'
            },
        ),
    ]

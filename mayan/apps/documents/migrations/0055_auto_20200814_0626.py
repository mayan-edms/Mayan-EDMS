from django.db import migrations, models

import mayan.apps.common.validators
import mayan.apps.documents.classes
import mayan.apps.documents.models.document_file_models
import mayan.apps.storage.classes


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0054_trasheddocument'),
    ]

    operations = [
        migrations.AddField(
            model_name='documenttype',
            name='filename_generator_backend',
            field=models.CharField(
                default='uuid',
                help_text='The class responsible for producing the actual '
                'filename used to store the uploaded documents.',
                max_length=224, verbose_name='Filename generator backend'
            ),
        ),
        migrations.AddField(
            model_name='documenttype',
            name='filename_generator_backend_arguments',
            field=models.TextField(
                blank=True, help_text='The arguments for the filename '
                'generator backend as a YAML dictionary.', validators=[
                    mayan.apps.common.validators.YAMLValidator()
                ], verbose_name='Filename generator backend arguments'
            ),
        ),
        migrations.AlterField(
            model_name='documentversion',
            name='file',
            field=models.FileField(
                storage=mayan.apps.storage.classes.DefinedStorageLazy(
                    name='documents__documentversion'
                ), upload_to=mayan.apps.documents.models.document_file_models.upload_to,
                verbose_name='File'
            ),
        ),
    ]

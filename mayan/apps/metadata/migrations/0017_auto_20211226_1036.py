from django.db import migrations, models
import mayan.apps.common.validators


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0016_auto_20211226_0905'),
    ]

    operations = [
        migrations.AddField(
            model_name='metadatatype', name='parser_arguments',
            field=models.TextField(
                blank=True, help_text='Enter the arguments for the '
                'parser in YAML format.', validators=[
                    mayan.apps.common.validators.YAMLValidator()
                ], verbose_name='Parser arguments'
            ),
        ),
        migrations.AlterField(
            model_name='metadatatype', name='parser',
            field=models.CharField(
                blank=True, help_text='The parser will reformat the '
                'value entered to conform to the expected format.',
                max_length=224, verbose_name='Parser'
            ),
        ),
        migrations.AlterField(
            model_name='metadatatype', name='validation',
            field=models.CharField(
                blank=True, help_text='The validator will reject '
                'data entry if the value entered does not conform to '
                'the expected format.', max_length=224,
                verbose_name='Validator'
            ),
        ),
    ]

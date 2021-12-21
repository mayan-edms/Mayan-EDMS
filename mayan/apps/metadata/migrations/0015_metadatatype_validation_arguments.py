from django.db import migrations, models
import mayan.apps.common.validators


class Migration(migrations.Migration):

    dependencies = [
        ('metadata', '0014_auto_20200705_0417')
    ]

    operations = [
        migrations.AddField(
            model_name='metadatatype',
            name='validation_arguments',
            field=models.TextField(
                blank=True, help_text='Enter the arguments for the '
                'validator in YAML format.', validators=[
                    mayan.apps.common.validators.YAMLValidator()
                ], verbose_name='Validator arguments'
            )
        )
    ]

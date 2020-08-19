from django.db import migrations, models
import mayan.apps.common.validators


class Migration(migrations.Migration):
    dependencies = [
        ('converter', '0018_asset'),
    ]

    operations = [
        migrations.AlterField(
            model_name='layertransformation',
            name='arguments',
            field=models.TextField(
                blank=True, help_text='Enter the arguments for the '
                'transformation as a YAML dictionary. ie: {"degrees": 180}',
                validators=[mayan.apps.common.validators.YAMLValidator()],
                verbose_name='Arguments'
            ),
        ),
    ]

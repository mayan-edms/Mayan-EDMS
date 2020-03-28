from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('sources', '0011_sanescanner'),
    ]

    operations = [
        migrations.AddField(
            model_name='sanescanner',
            name='mode',
            field=models.CharField(
                choices=[
                    ('lineart', 'Lineart'), ('monochrome', 'Monochrome'),
                    ('color', 'Color')
                ], default='color', max_length=16, verbose_name='Mode'
            ),
        ),
        migrations.AddField(
            model_name='sanescanner',
            name='resolution',
            field=models.PositiveIntegerField(
                default=300,
                help_text='Sets the resolution of the scanned image in '
                'DPI (dots per inch).',
                verbose_name='Resolution'
            ),
        ),
    ]

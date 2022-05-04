from django.db import migrations

from ..compatibility import RGBColorField


class Migration(migrations.Migration):
    dependencies = [
        ('tags', '0004_auto_20150717_2336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=RGBColorField(verbose_name='Color'),
            preserve_default=True,
        ),
    ]

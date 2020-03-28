from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('document_indexing', '0015_auto_20190429_1922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='index',
            name='label',
            field=models.CharField(
                help_text='Short description of this index.',
                max_length=128, unique=True, verbose_name='Label'
            ),
        ),
    ]

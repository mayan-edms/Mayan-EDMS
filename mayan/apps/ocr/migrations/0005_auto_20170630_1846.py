from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('ocr', '0004_documenttypesettings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentversionocrerror',
            name='document_version',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='ocr_errors', to='documents.DocumentVersion',
                verbose_name='Document version'
            ),
        ),
    ]

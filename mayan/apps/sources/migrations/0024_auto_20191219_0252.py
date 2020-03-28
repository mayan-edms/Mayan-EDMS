from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('sources', '0023_auto_20191213_0044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='intervalbasemodel',
            name='document_type',
            field=models.ForeignKey(
                help_text='Assign a document type to documents uploaded '
                'from this source.',
                on_delete=django.db.models.deletion.CASCADE,
                related_name='interval_sources', to='documents.DocumentType',
                verbose_name='Document type'
            ),
        ),
    ]

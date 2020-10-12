from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0063_auto_20201012_0320'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentVersionPageResult',
            fields=[
            ],
            options={
                'verbose_name': 'Document version page',
                'verbose_name_plural': 'Document version pages',
                'ordering': ('document_version__document', 'page_number'),
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('documents.documentversionpage',),
        ),
        migrations.AlterField(
            model_name='documentversionpage',
            name='document_version',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='version_pages', to='documents.DocumentVersion',
                verbose_name='Document version'
            ),
        ),
    ]

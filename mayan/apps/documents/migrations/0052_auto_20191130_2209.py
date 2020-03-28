from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0051_documentpage_enabled'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentpage',
            name='document_version',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='version_pages', to='documents.DocumentVersion',
                verbose_name='Document version'
            ),
        ),
    ]

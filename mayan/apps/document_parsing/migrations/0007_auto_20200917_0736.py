from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('document_parsing', '0006_rename_documentversionparseerror_model'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='documentfileparseerror',
            options={'ordering': ('datetime_submitted',), 'verbose_name': 'Document file parse error', 'verbose_name_plural': 'Document file parse errors'},
        ),
        migrations.AlterField(
            model_name='documentfileparseerror',
            name='document_file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parsing_errors', to='documents.DocumentFile', verbose_name='Document file'),
        ),
    ]

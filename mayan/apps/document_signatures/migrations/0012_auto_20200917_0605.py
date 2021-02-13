from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('document_signatures', '0011_rename_signaturebasemodel_field'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='detachedsignature',
            options={
                'verbose_name': 'Document file detached signature',
                'verbose_name_plural': 'Document file detached signatures'
            },
        ),
        migrations.AlterModelOptions(
            name='embeddedsignature',
            options={
                'verbose_name': 'Document file embedded signature',
                'verbose_name_plural': 'Document file embedded signatures'
            },
        ),
        migrations.AlterModelOptions(
            name='signaturebasemodel',
            options={
                'ordering': ('pk',),
                'verbose_name': 'Document file signature',
                'verbose_name_plural': 'Document file signatures'
            },
        ),
        migrations.AlterField(
            model_name='signaturebasemodel',
            name='document_file',
            field=models.ForeignKey(
                editable=False, on_delete=django.db.models.deletion.CASCADE,
                related_name='signatures', to='documents.DocumentFile',
                verbose_name='Document file'
            ),
        ),
    ]

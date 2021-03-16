from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0075_delete_duplicateddocumentold'),
        ('duplicates', '0007_auto_20201130_0828'),
    ]

    operations = [
        migrations.CreateModel(
            name='DuplicateSourceDocument',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('documents.document',),
        ),
        migrations.CreateModel(
            name='DuplicateTargetDocument',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('documents.document',),
        ),
        migrations.AlterField(
            model_name='duplicatebackendentry',
            name='document',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='duplicates', to='documents.Document',
                verbose_name='Document'
            ),
        ),
        migrations.AlterUniqueTogether(
            name='duplicatebackendentry',
            unique_together={('stored_backend', 'document')},
        ),
    ]

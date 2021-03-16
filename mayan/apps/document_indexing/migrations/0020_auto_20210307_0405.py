from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('document_indexing', '0019_auto_20200910_0816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='index',
            name='document_types',
            field=models.ManyToManyField(
                related_name='index_templates', to='documents.DocumentType',
                verbose_name='Document types'
            ),
        ),
    ]

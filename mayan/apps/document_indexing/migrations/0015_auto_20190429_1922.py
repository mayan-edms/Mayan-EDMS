from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('document_indexing', '0014_auto_20180823_2353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='index',
            name='document_types',
            field=models.ManyToManyField(
                related_name='indexes', to='documents.DocumentType',
                verbose_name='Document types'
            ),
        ),
    ]

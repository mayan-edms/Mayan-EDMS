from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('linking', '0007_auto_20180823_2353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smartlink',
            name='document_types',
            field=models.ManyToManyField(
                related_name='smart_links', to='documents.DocumentType',
                verbose_name='Document types'
            ),
        ),
    ]

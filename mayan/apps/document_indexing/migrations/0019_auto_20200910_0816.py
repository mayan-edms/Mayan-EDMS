from django.db import migrations
import django.db.models.deletion

import mptt.fields


class Migration(migrations.Migration):
    dependencies = [
        ('document_indexing', '0018_auto_20200402_0647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indexinstancenode',
            name='parent',
            field=mptt.fields.TreeForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='children',
                to='document_indexing.IndexInstanceNode'
            ),
        ),
        migrations.AlterField(
            model_name='indextemplatenode',
            name='parent',
            field=mptt.fields.TreeForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='children',
                to='document_indexing.IndexTemplateNode'
            ),
        ),
    ]

from django.db import migrations
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):
    dependencies = [
        ('document_indexing', '0024_auto_20210822_0052')
    ]

    operations = [
        migrations.AlterField(
            model_name='indextemplatenode',
            name='parent',
            field=mptt.fields.TreeForeignKey(
                blank=True,
                help_text='Parent index template node of this node.',
                null=True, on_delete=django.db.models.deletion.CASCADE,
                related_name='children',
                to='document_indexing.IndexTemplateNode'
            )
        )
    ]

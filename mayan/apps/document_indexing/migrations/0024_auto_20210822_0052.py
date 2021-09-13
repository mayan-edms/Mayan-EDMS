from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('document_indexing', '0023_auto_20210821_2059'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='indexinstancenode',
            unique_together={('index_template_node', 'parent', 'value')},
        ),
        migrations.AlterModelOptions(
            name='indextemplate',
            options={
                'ordering': ('label',), 'verbose_name': 'Index template',
                'verbose_name_plural': 'Index templates'
            },
        ),
        migrations.AlterField(
            model_name='indextemplatenode',
            name='expression',
            field=models.TextField(
                help_text="Enter a template to render. Use Django's "
                "default templating language.",
                verbose_name='Indexing expression'
            ),
        ),
        migrations.AlterField(
            model_name='indextemplatenode',
            name='index',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='index_template_nodes',
                to='document_indexing.IndexTemplate', verbose_name='Index'
            ),
        ),
        migrations.AlterModelOptions(
            name='indextemplatenode',
            options={
                'verbose_name': 'Index template node',
                'verbose_name_plural': 'Index template nodes'
            },
        )
    ]

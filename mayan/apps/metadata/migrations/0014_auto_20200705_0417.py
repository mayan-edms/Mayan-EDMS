from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('metadata', '0013_auto_20191005_0646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documenttypemetadatatype',
            name='metadata_type',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='document_types', to='metadata.MetadataType',
                verbose_name='Metadata type'
            ),
        ),
        migrations.AlterField(
            model_name='metadatatype',
            name='default',
            field=models.CharField(
                blank=True, help_text='Enter a template to render.',
                max_length=128, null=True, verbose_name='Default'
            ),
        ),
        migrations.AlterField(
            model_name='metadatatype',
            name='lookup',
            field=models.TextField(
                blank=True, help_text='Enter a template to render. Must '
                'result in a comma delimited string.', null=True,
                verbose_name='Lookup'
            ),
        ),
    ]

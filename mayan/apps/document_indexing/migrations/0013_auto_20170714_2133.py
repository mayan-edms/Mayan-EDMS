from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('document_indexing', '0012_auto_20170530_0728'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='index',
            options={
                'ordering': ('label',), 'verbose_name': 'Index',
                'verbose_name_plural': 'Indexes'
            },
        ),
    ]

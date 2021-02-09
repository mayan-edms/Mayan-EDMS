from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('document_indexing', '0017_auto_20200330_0851'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndexInstanceNodeSearchResult',
            fields=[
            ],
            options={
                'verbose_name': 'Index instance node',
                'verbose_name_plural': 'Index instance nodes',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('document_indexing.indexinstancenode',),
        ),
        migrations.AlterModelOptions(
            name='indexinstancenode',
            options={
                'verbose_name': 'Index instance node',
                'verbose_name_plural': 'Indexes instances node'
            },
        ),
    ]

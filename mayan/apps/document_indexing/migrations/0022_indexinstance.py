from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('document_indexing', '0021_auto_20210307_0439'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndexInstance',
            fields=[
            ],
            options={
                'verbose_name': 'Index instance',
                'verbose_name_plural': 'Index instances',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('document_indexing.indextemplate',),
        ),
    ]

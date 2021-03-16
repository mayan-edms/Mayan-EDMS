from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0058_auto_20200916_1146'),
    ]
    operations = [
        migrations.DeleteModel(
            name='DocumentPageResult',
        ),
        migrations.RenameModel(
            old_name='DocumentPage',
            new_name='DocumentFilePage',
        ),
        migrations.CreateModel(
            name='DocumentFilePageResult',
            fields=[
            ],
            options={
                'verbose_name': 'Document file page',
                'verbose_name_plural': 'Document file pages',
                'ordering': ('document_file__document', 'page_number'),
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('documents.documentfilepage',),
        ),
        migrations.AlterModelOptions(
            name='documentfilepage',
            options={
                'ordering': ('page_number',),
                'verbose_name': 'Document file page',
                'verbose_name_plural': 'Document file pages'
            },
        ),
    ]

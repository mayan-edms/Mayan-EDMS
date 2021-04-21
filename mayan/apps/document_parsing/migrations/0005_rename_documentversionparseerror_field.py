from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('document_parsing', '0004_auto_20180917_0645'),
        ('documents', '0057_auto_20200916_1057')
    ]

    operations = [
        migrations.RenameField(
            model_name='documentversionparseerror',
            old_name='document_version',
            new_name='document_file',
        ),
    ]

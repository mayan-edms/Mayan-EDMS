from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0057_auto_20200916_1057'),
        ('document_signatures', '0010_auto_20191201_0146')
    ]

    operations = [
        migrations.RenameField(
            model_name='signaturebasemodel',
            old_name='document_version',
            new_name='document_file',
        ),
    ]

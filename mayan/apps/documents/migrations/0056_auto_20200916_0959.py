from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        #('file_metadata', '0003_auto_20191226_0606'),
        #('document_signatures', '0010_auto_20191201_0146'),
        #('document_parsing', '0004_auto_20180917_0645'),
        #('ocr', '0008_auto_20180917_0646'),
        ('documents', '0055_auto_20200814_0626'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DocumentVersion',
            new_name='DocumentFile',
        ),
    ]

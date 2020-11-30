from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0072_auto_20201128_0919'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DuplicatedDocument',
            new_name='DuplicatedDocumentOld',
        ),
    ]

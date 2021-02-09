from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0064_auto_20201012_0544'),
        ('ocr', '0011_auto_20201012_0917'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DocumentTypeSettings',
            new_name='DocumentTypeOCRSettings',
        ),
    ]

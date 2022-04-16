from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('ocr', '0010_auto_20210304_1215')
    ]

    operations = [
        migrations.DeleteModel(
            name='DocumentVersionOCRError',
        )
    ]

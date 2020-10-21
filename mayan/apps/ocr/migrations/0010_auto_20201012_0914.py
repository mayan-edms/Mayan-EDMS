from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('ocr', '0009_auto_20201012_0912'),
    ]

    operations = [
        migrations.RenameField(
            model_name='documentversionpageocrcontent',
            old_name='document_page',
            new_name='document_version_page',
        ),
    ]

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('document_parsing', '0005_rename_documentversionparseerror_field'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DocumentVersionParseError',
            new_name='DocumentFileParseError',
        )
    ]

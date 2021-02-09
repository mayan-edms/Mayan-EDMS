from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0064_auto_20201012_0544'),
        ('document_parsing', '0007_auto_20200917_0736'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DocumentPageContent',
            new_name='DocumentFilePageContent',
        ),
    ]

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('document_parsing', '0008_auto_20201012_0707'),
    ]

    operations = [
        migrations.RenameField(
            model_name='documentfilepagecontent',
            old_name='document_page',
            new_name='document_file_page',
        ),
    ]

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0075_delete_duplicateddocumentold'),
        ('document_indexing', '0020_auto_20210307_0405'),
    ]

    operations = [
        migrations.DeleteModel(
            name='IndexInstance',
        ),
        migrations.RenameModel(
            old_name='Index',
            new_name='IndexTemplate',
        ),
    ]

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0074_auto_20201130_0341'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DuplicatedDocumentOld',
        ),
    ]

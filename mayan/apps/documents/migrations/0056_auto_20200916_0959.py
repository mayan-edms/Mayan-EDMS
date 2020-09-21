from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0055_auto_20200814_0626'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DocumentVersion',
            new_name='DocumentFile',
        ),
    ]

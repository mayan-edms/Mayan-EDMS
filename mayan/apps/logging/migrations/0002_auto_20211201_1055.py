from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('logging', '0001_initial')
    ]

    operations = [
        migrations.RenameModel(
            old_name='ErrorLog',
            new_name='StoredErrorLog'
        )
    ]

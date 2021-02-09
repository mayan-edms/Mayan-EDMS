from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('common', '0016_delete_shareduploadedfile'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ErrorLogEntry',
        ),
    ]

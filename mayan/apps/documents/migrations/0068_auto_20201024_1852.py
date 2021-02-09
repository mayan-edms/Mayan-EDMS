from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0067_auto_20201024_1120'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DeletedDocument',
        ),
        migrations.RenameField(
            model_name='document',
            old_name='deleted_date_time',
            new_name='trashed_date_time',
        ),
    ]

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('logging', '0005_auto_20220119_0518')
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='errorlogpartition',
            unique_together={
                ('error_log', 'content_type', 'object_id'),
                ('error_log', 'name')
            }
        )
    ]

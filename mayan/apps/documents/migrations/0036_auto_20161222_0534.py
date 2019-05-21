from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0035_auto_20161102_0633'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newversionblock',
            name='document',
        ),
        migrations.DeleteModel(
            name='NewVersionBlock',
        ),
    ]

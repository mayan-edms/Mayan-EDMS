from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('document_indexing', '0023_auto_20210821_2059'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='indexinstancenode',
            unique_together={('parent', 'value')},
        ),
    ]

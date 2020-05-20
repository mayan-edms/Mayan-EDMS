from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('document_indexing', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='index',
            name='name',
        ),
    ]

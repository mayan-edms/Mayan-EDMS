from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('document_parsing', '0010_auto_20201012_0708')
    ]

    operations = [
        migrations.DeleteModel(
            name='DocumentFileParseError',
        )
    ]

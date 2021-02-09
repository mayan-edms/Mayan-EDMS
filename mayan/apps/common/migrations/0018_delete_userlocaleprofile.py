from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('common', '0017_delete_errorlogentry'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserLocaleProfile',
        ),
    ]

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0070_auto_20201128_0249'),
    ]

    operations = [
        migrations.RenameField(
            model_name='document',
            old_name='date_added',
            new_name='datetime_created',
        ),
    ]

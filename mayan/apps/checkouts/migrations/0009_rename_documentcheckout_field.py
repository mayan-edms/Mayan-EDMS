from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('checkouts', '0008_checkedoutdocument')
    ]

    operations = [
        migrations.RenameField(
            model_name='documentcheckout',
            old_name='block_new_version',
            new_name='block_new_file',
        ),
    ]

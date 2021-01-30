from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('document_comments', '0004_auto_20150920_0202'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='comment',
            new_name='text',
        ),
    ]

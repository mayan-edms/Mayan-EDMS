from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('common', '0015_auto_20200501_0631'),
        ('storage', '0002_auto_20200528_0826')
    ]

    operations = [
        migrations.DeleteModel(
            name='SharedUploadedFile',
        ),
    ]

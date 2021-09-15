from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('sources', '0024_auto_20191219_0252'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SourceLog',
        ),
    ]

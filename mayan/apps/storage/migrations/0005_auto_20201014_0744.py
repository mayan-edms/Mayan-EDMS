from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('storage', '0004_downloadfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shareduploadedfile',
            name='filename',
            field=models.CharField(db_index=True, max_length=255, verbose_name='Filename'),
        ),
    ]

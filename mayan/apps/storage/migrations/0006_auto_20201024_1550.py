from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('storage', '0005_auto_20201014_0744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shareduploadedfile',
            name='filename',
            field=models.CharField(blank=True, max_length=255, verbose_name='Filename'),
        ),
    ]

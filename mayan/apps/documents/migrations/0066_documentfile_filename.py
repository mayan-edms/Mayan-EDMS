from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0065_documentversion_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentfile',
            name='filename',
            field=models.CharField(
                default='', max_length=255, verbose_name='Filename'
            ),
            preserve_default=False,
        ),
    ]

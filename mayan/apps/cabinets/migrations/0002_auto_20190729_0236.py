from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('cabinets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cabinet', name='label', field=models.CharField(
                help_text='A short text used to identify the cabinet.',
                max_length=128, verbose_name='Label'
            ),
        ),
    ]

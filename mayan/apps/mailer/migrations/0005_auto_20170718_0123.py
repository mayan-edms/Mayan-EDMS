from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('mailer', '0004_auto_20170714_2133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermailer',
            name='label',
            field=models.CharField(
                max_length=128, unique=True, verbose_name='Label'
            ),
        ),
    ]

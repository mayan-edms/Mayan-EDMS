from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('mailer', '0003_auto_20170703_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermailer',
            name='default',
            field=models.BooleanField(
                default=True, help_text='If default, this mailing profile '
                'will be pre-selected on the document mailing form.',
                verbose_name='Default'
            ),
        ),
    ]

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('mailer', '0005_auto_20170718_0123'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usermailer',
            options={
                'ordering': ('label',),
                'verbose_name': 'Mailing profile',
                'verbose_name_plural': 'Mailing profiles'
            },
        ),
        migrations.AlterField(
            model_name='usermailer',
            name='label',
            field=models.CharField(
                help_text='A short text describing the mailing profile.',
                max_length=128, unique=True, verbose_name='Label'
            ),
        ),
    ]

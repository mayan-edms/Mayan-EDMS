from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('mailer', '0002_usermailer_usermailerlogentry'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermailer',
            name='enabled',
            field=models.BooleanField(default=True, verbose_name='Enabled'),
        ),
        migrations.AlterField(
            model_name='usermailerlogentry',
            name='user_mailer',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='error_log', to='mailer.UserMailer',
                verbose_name='User mailer'
            ),
        ),
    ]

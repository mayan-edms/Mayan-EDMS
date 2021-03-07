from django.db import migrations, models
import mayan.apps.databases.model_mixins


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('motd', '0005_auto_20160510_0025'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True, primary_key=True,
                        serialize=False, verbose_name='ID'
                    )
                ),
                (
                    'label', models.CharField(
                        help_text='Short description of this announcement.',
                        max_length=32, verbose_name='Label'
                    )
                ),
                (
                    'text', models.TextField(
                        help_text='The actual test to be displayed.',
                        verbose_name='Text'
                    )
                ),
                (
                    'enabled', models.BooleanField(
                        default=True, verbose_name='Enabled'
                    )
                ),
                (
                    'start_datetime', models.DateTimeField(
                        blank=True, help_text='Date and time after which '
                        'this announcement will be displayed.', null=True,
                        verbose_name='Start date time'
                    )
                ),
                (
                    'end_datetime', models.DateTimeField(
                        blank=True, help_text='Date and time until when '
                        'this announcement is to be displayed.', null=True,
                        verbose_name='End date time'
                    )
                ),
            ],
            options={
                'verbose_name': 'Announcement',
                'verbose_name_plural': 'Announcements',
            },
            bases=(
                mayan.apps.databases.model_mixins.ExtraDataModelMixin,
                models.Model
            ),
        ),
    ]

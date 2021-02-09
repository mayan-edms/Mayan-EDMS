from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Quota',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True, primary_key=True, serialize=False,
                        verbose_name='ID'
                    )
                ),
                (
                    'backend_path', models.CharField(
                        help_text='The dotted Python path to the backend '
                        'class.', max_length=255, verbose_name='Backend path'
                    )
                ),
                (
                    'backend_data', models.TextField(
                        blank=True, verbose_name='Backend data'
                    )
                ),
                (
                    'enabled', models.BooleanField(
                        default=True, help_text='Allow quick disable or '
                        'enable of the quota.', verbose_name='Enabled'
                    )
                ),
            ],
            options={
                'verbose_name': 'Quota',
                'verbose_name_plural': 'Quotas',
            },
        ),
    ]

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('duplicates', '0003_auto_20201130_0431'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoredDuplicateBackend',
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
                        'class.', max_length=128, verbose_name='Backend path'
                    )
                ),
                (
                    'backend_data', models.TextField(
                        blank=True, verbose_name='Backend data'
                    )
                ),
            ],
            options={
                'verbose_name': 'Stored duplicate backend',
                'verbose_name_plural': 'Stored duplicate backends',
            },
        ),
    ]

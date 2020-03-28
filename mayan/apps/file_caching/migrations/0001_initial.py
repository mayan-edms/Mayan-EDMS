from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cache',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True, primary_key=True, serialize=False,
                        verbose_name='ID'
                    )
                ),
                (
                    'name', models.CharField(
                        max_length=128, unique=True, verbose_name='Name'
                    )
                ),
                (
                    'label', models.CharField(
                        max_length=128, verbose_name='Label'
                    )
                ),
                (
                    'maximum_size', models.PositiveIntegerField(
                        verbose_name='Maximum size'
                    )
                ),
                (
                    'storage_instance_path', models.CharField(
                        max_length=255, unique=True,
                        verbose_name='Storage instance path'
                    )
                ),
            ],
            options={
                'verbose_name': 'Cache',
                'verbose_name_plural': 'Caches',
            },
        ),
        migrations.CreateModel(
            name='CachePartition',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True, primary_key=True, serialize=False,
                        verbose_name='ID'
                    )
                ),
                (
                    'name', models.CharField(
                        max_length=128, verbose_name='Name'
                    )
                ),
                (
                    'cache', models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='partitions', to='file_caching.Cache',
                        verbose_name='Cache'
                    )
                ),
            ],
            options={
                'verbose_name': 'Cache partition',
                'verbose_name_plural': 'Cache partitions',
            },
        ),
        migrations.CreateModel(
            name='CachePartitionFile',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True, primary_key=True, serialize=False,
                        verbose_name='ID'
                    )
                ),
                (
                    'datetime', models.DateTimeField(
                        auto_now_add=True, db_index=True,
                        verbose_name='Date time'
                    )
                ),
                (
                    'filename', models.CharField(
                        max_length=255, verbose_name='Filename'
                    )
                ),
                (
                    'file_size', models.PositiveIntegerField(
                        default=0, verbose_name='File size'
                    )
                ),
                (
                    'partition', models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='files',
                        to='file_caching.CachePartition',
                        verbose_name='Cache partition'
                    )
                ),
            ],
            options={
                'get_latest_by': 'datetime',
                'verbose_name': 'Cache partition file',
                'verbose_name_plural': 'Cache partition files',
            },
        ),
        migrations.AlterUniqueTogether(
            name='cachepartitionfile',
            unique_together=set([('partition', 'filename')]),
        ),
        migrations.AlterUniqueTogether(
            name='cachepartition',
            unique_together=set([('cache', 'name')]),
        ),
    ]

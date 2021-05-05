from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('file_caching', '0007_cachepartitionfile_hits'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cachepartitionfile',
            name='hits',
            field=models.PositiveIntegerField(
                db_index=True, default=0, help_text='Times this cache '
                'partition file has been accessed.', verbose_name='Hits'
            ),
        ),
    ]

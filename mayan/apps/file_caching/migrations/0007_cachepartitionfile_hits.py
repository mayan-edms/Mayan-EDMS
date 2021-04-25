from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('file_caching', '0006_auto_20200322_0626'),
    ]

    operations = [
        migrations.AddField(
            model_name='cachepartitionfile', name='hits',
            field=models.PositiveIntegerField(
                default=0, help_text='Times this cache partition file has '
                'been accessed.', verbose_name='Hits'
            ),
        ),
    ]

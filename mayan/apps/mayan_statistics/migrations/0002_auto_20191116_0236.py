from __future__ import unicode_literals

from django.db import migrations, models


def operation_rename_duplicates(apps, schema_editor):
    StatisticResult = apps.get_model(
        app_label='mayan_statistics', model_name='StatisticResult'
    )
    slugs = []

    for entry in StatisticResult.objects.using(schema_editor.connection.alias).all():
        if entry.slug in slugs:
            counter = 1
            while(True):
                attempt = '{}_{}'.format(entry.slug, counter)
                if attempt not in slugs:
                    break
                else:
                    counter = counter + 1

            entry.slug = attempt
            entry.save()

        slugs.append(entry.slug)


class Migration(migrations.Migration):

    dependencies = [
        ('mayan_statistics', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            code=operation_rename_duplicates,
            reverse_code=migrations.RunPython.noop
        ),
        migrations.AlterField(
            model_name='statisticresult',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='Slug'),
        ),
    ]

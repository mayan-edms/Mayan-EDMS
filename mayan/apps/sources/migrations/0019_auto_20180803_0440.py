from __future__ import unicode_literals

from django.db import migrations, models


def operation_make_labels_unique(apps, schema_editor):
    Source = apps.get_model(app_label='sources', model_name='Source')

    for source in Source.objects.using(schema_editor.connection.alias).all():
        # Look for sources with the same label
        duplicate_queryset = Source.objects.using(
            schema_editor.connection.alias
        ).filter(label=source.label).exclude(pk=source.pk)
        if duplicate_queryset:
            # If a duplicate is found, append the id to the original source
            # label
            source.label = '{}__{}'.format(source.label, source.pk)
            source.save()


def operation_make_labels_unique_reverse(apps, schema_editor):
    Source = apps.get_model(app_label='sources', model_name='Source')

    for source in Source.objects.using(schema_editor.connection.alias).all():
        if source.label.endswith('__{}'.format(source.pk)):
            source.label = source.label.replace('__{}'.format(source.pk), '')
            source.save()


class Migration(migrations.Migration):

    dependencies = [
        ('sources', '0018_auto_20180608_0057'),
    ]

    operations = [
        migrations.RunPython(
            code=operation_make_labels_unique,
            reverse_code=operation_make_labels_unique_reverse
        ),
        migrations.AlterField(
            model_name='source',
            name='label',
            field=models.CharField(
                db_index=True, max_length=64, unique=True, verbose_name='Label'
            ),
        ),
    ]

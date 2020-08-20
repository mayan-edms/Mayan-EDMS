from django.db import migrations, models


def operation_make_labels_unique(apps, schema_editor):
    WebLink = apps.get_model(app_label='web_links', model_name='WebLink')

    for web_link in WebLink.objects.using(schema_editor.connection.alias).all():
        # Look for instances with the same label
        duplicate_queryset = WebLink.objects.using(
            schema_editor.connection.alias
        ).filter(label=web_link.label).exclude(pk=web_link.pk)
        if duplicate_queryset:
            # If a duplicate is found, append the id to the original instance
            # label
            web_link.label = '{}__{}'.format(web_link.label, web_link.pk)
            web_link.save()


def operation_make_labels_unique_reverse(apps, schema_editor):
    WebLink = apps.get_model(app_label='web_links', model_name='WebLink')

    for web_link in WebLink.objects.using(schema_editor.connection.alias).all():
        if web_link.label.endswith('__{}'.format(web_link.pk)):
            web_link.label = web_link.label.replace(
                '__{}'.format(web_link.pk), ''
            )
            web_link.save()


class Migration(migrations.Migration):
    dependencies = [
        ('web_links', '0003_auto_20191211_0233'),
    ]

    operations = [
        migrations.RunPython(
            code=operation_make_labels_unique,
            reverse_code=operation_make_labels_unique_reverse
        ),
    ]

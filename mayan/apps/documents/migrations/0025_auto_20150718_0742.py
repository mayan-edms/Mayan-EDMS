import pycountry

from django.db import migrations


def operation_change_bibliographic_to_terminology(apps, schema_editor):
    Document = apps.get_model(app_label='documents', model_name='Document')

    for document in Document.objects.using(schema_editor.connection.alias).all():
        try:
            language = pycountry.languages.get(bibliographic=document.language)
        except KeyError:
            # The pycountry version used doesn't support the 'bibliographic'
            # key. Reset the document's language to English.
            # GitHub issue #250
            # https://github.com/mayan-edms/mayan-edms/issues/250
            document.language = 'eng'
            document.save()
        else:
            document.language = language.terminology
            document.save()


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0024_auto_20150715_0714'),
    ]

    operations = [
        migrations.RunPython(code=operation_change_bibliographic_to_terminology),
    ]

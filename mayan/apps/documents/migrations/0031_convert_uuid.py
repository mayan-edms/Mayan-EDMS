import uuid

from django.db import migrations


def operation_convert_uuid_to_hex(apps, schema_editor):
    Document = apps.get_model(app_label='documents', model_name='Document')

    for document in Document.objects.using(alias=schema_editor.connection.alias).all():
        document.uuid = uuid.UUID(document.uuid).hex
        document.save()


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0030_auto_20160309_1837'),
    ]

    operations = [
        migrations.RunPython(code=operation_convert_uuid_to_hex),
    ]

from django.db import models, migrations


def operation_make_existing_documents_not_stubs(apps, schema_editor):
    Document = apps.get_model(app_label='documents', model_name='Document')

    for document in Document.objects.using(alias=schema_editor.connection.alias).all():
        document.is_stub = False
        document.save()


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0012_auto_20150705_0347'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='is_stub',
            field=models.BooleanField(
                default=True, verbose_name='Is stub?', editable=False
            ),
            preserve_default=True,
        ),
        migrations.RunPython(code=operation_make_existing_documents_not_stubs),
    ]

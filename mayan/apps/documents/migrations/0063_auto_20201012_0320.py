from django.db import migrations


def operation_document_version_page_create(apps, schema_editor):
    ContentType = apps.get_model(
        app_label='contenttypes', model_name='ContentType'
    )
    DocumentFilePage = apps.get_model(
        app_label='documents', model_name='DocumentFilePage'
    )
    DocumentVersion = apps.get_model(
        app_label='documents', model_name='DocumentVersion'
    )

    content_type = ContentType.objects.get_for_model(model=DocumentFilePage)
    content_type_id = content_type.id
    cursor_main = schema_editor.connection.cursor()
    cursor_document_version_page = schema_editor.connection.cursor()

    query = '''
    SELECT
        "documents_documentfile"."document_id",
        "documents_documentfilepage"."document_file_id",
        "documents_documentfilepage"."id"
    FROM "documents_documentfilepage"
    INNER JOIN "documents_documentfile" ON (
        "documents_documentfilepage"."document_file_id" = "documents_documentfile"."id"
    ) ORDER BY "documents_documentfilepage"."id" ASC
    '''
    cursor_main.execute(query)

    class DummyDocumentVersion:
        def save(self):
            """Does not do anything."""

    document_file_id_last = None
    document_id_last = None
    document_version = DummyDocumentVersion()
    document_version_page_insert_query = '''
        INSERT INTO documents_documentversionpage (
            document_version_id,content_type_id,object_id,page_number
        ) VALUES {};
    '''
    document_version_page_values = []
    page_number = 1

    for row in cursor_main.fetchall():
        document_id, document_file_id, document_file_page_id = row

        if document_id_last != document_id:
            document_version.active = True
            document_version.save()
            document_id_last = document_id

        if document_file_id_last != document_file_id:
            document_version = DocumentVersion.objects.create(document_id=document_id)
            document_version_id = document_version.pk
            document_file_id_last = document_file_id
            if document_version_page_values:
                final_query = document_version_page_insert_query.format(
                    ','.join(['(%s,%s,%s,%s)'] * (page_number - 1))
                )

                page_number = 1

                cursor_document_version_page.execute(
                    final_query, document_version_page_values
                )

            document_version_page_values = []

        document_version_page_values.extend(
            (
                document_version_id, content_type_id, document_file_page_id,
                page_number
            )
        )

        page_number = page_number + 1

    if page_number > 1:
        final_query = document_version_page_insert_query.format(
            ','.join(['(%s,%s,%s,%s)'] * (page_number - 1))
        )
        cursor_document_version_page.execute(
            final_query, document_version_page_values
        )


def operation_document_version_page_create_reverse(apps, schema_editor):
    DocumentVersionPage = apps.get_model(
        app_label='documents', model_name='DocumentVersionPage'
    )

    DocumentVersionPage.objects.using(schema_editor.connection.alias).all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('documents', '0062_auto_20200920_0614'),
    ]

    operations = [
        migrations.RunPython(
            code=operation_document_version_page_create,
            reverse_code=operation_document_version_page_create_reverse
        ),
    ]

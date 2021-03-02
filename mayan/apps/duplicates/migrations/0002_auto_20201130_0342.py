from django.db import migrations


def operation_duplicated_document_old_copy(apps, schema_editor):
    DuplicatedDocument = apps.get_model(
        app_label='duplicates', model_name='DuplicatedDocument'
    )

    cursor_primary = schema_editor.connection.cursor()
    cursor_secondary = schema_editor.connection.cursor()
    query = '''
        SELECT
            "documents_duplicateddocumentold"."id",
            "documents_duplicateddocumentold"."datetime_added",
            "documents_duplicateddocumentold"."document_id"
        FROM "documents_duplicateddocumentold"
    '''
    cursor_primary.execute(query)

    for row in cursor_primary.fetchall():
        new_instance = DuplicatedDocument.objects.create(
            document_id=row[2],
            datetime_added=row[1]
        )

        query = '''
            SELECT
                "documents_duplicateddocumentold_documents"."document_id"
            FROM
                "documents_duplicateddocumentold_documents"
            WHERE
                "documents_duplicateddocumentold_documents"."duplicateddocumentold_id" = %s
        '''
        cursor_secondary.execute(query, (row[0],))
        results = cursor_secondary.fetchall()

        if results:
            insert_query = '''
                INSERT INTO duplicates_duplicateddocument_documents (
                    duplicateddocument_id,document_id
                ) VALUES {};
            '''
            insert_query_final = insert_query.format(
                ','.join(['(%s,%s)'] * len(results))
            )
            data = []
            for result in results:
                data.append(new_instance.pk)
                data.append(result[0])

            cursor_secondary.execute(
                insert_query_final, data
            )

    query = '''
        DELETE FROM "documents_duplicateddocumentold_documents";
    '''
    cursor_secondary.execute(query)

    query = '''
        DELETE FROM "documents_duplicateddocumentold";
    '''
    cursor_secondary.execute(query)


def operation_duplicated_document_old_copy_reverse(apps, schema_editor):
    DuplicatedDocumentOld = apps.get_model(
        app_label='documents', model_name='DuplicatedDocumentOld'
    )

    cursor_primary = schema_editor.connection.cursor()
    cursor_secondary = schema_editor.connection.cursor()
    query = '''
        SELECT
            "duplicates_duplicateddocument"."id",
            "duplicates_duplicateddocument"."datetime_added",
            "duplicates_duplicateddocument"."document_id"
        FROM "duplicates_duplicateddocument"
    '''
    cursor_primary.execute(query)

    for row in cursor_primary.fetchall():
        new_instance = DuplicatedDocumentOld.objects.create(
            document_id=row[2],
            datetime_added=row[1]
        )

        query = '''
            SELECT DISTINCT
                "duplicates_duplicateddocument_documents"."document_id"
            FROM
                "duplicates_duplicateddocument_documents"
            WHERE
                "duplicates_duplicateddocument_documents"."duplicateddocument_id" = %s
        '''
        cursor_secondary.execute(query, (row[0],))
        results = cursor_secondary.fetchall()

        if results:
            insert_query = '''
                INSERT INTO documents_duplicateddocumentold_documents (
                    duplicateddocumentold_id,document_id
                ) VALUES {};
            '''
            insert_query_final = insert_query.format(
                ','.join(['(%s,%s)'] * len(results))
            )
            data = []
            for result in results:
                data.append(new_instance.pk)
                data.append(result[0])

            cursor_secondary.execute(
                insert_query_final, data
            )

    query = '''
        DELETE FROM "duplicates_duplicateddocument_documents";
    '''
    cursor_secondary.execute(query)

    query = '''
        DELETE FROM "duplicates_duplicateddocument";
    '''
    cursor_secondary.execute(query)


class Migration(migrations.Migration):
    dependencies = [
        ('duplicates', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            code=operation_duplicated_document_old_copy,
            reverse_code=operation_duplicated_document_old_copy_reverse
        ),
    ]

    run_before = [
        ('documents', '0075_delete_duplicateddocumentold'),
    ]

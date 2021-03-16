from django.db import migrations
from django.utils.timezone import now


def operation_duplicated_document_old_copy(apps, schema_editor):
    # Remove duplicated entries.
    # DuplicatedDocument allowed duplicates, DuplicateBackendEntry does
    # not.
    cursor_primary = schema_editor.connection.cursor()
    cursor_secondary = schema_editor.connection.cursor()
    cursor_tertiary = schema_editor.connection.cursor()

    query = '''
        SELECT DISTINCT
            "documents_duplicateddocumentold"."document_id",
            "documents_duplicateddocumentold_documents"."document_id"
        FROM "documents_duplicateddocumentold"
        LEFT OUTER JOIN
            "documents_duplicateddocumentold_documents" ON (
                "documents_duplicateddocumentold"."id" = "documents_duplicateddocumentold_documents"."duplicateddocumentold_id"
            )
        ORDER BY "documents_duplicateddocumentold"."document_id" ASC
    '''
    cursor_primary.execute(query)

    document_insert_query = '''
        INSERT INTO duplicates_duplicateddocument_documents (
            duplicateddocument_id,document_id
        ) VALUES {};
    '''

    last_document_id = None
    document_list = []
    duplicated_document_query = '''
        INSERT INTO duplicates_duplicateddocument (
            document_id,datetime_added
        ) VALUES (%s,%s);
        SELECT "duplicates_duplicateddocument"."id" FROM
            "duplicates_duplicateddocument"
        WHERE
            "duplicates_duplicateddocument"."document_id" = %s;
    '''
    now_text = now()

    for row in cursor_primary.fetchall():
        if last_document_id != row[0]:
            cursor_tertiary.execute(
                duplicated_document_query, (row[0], now_text, row[0])
            )
            new_instance_pk = cursor_tertiary.fetchone()[0]

            if document_list:
                final_query = document_insert_query.format(
                    ('(%s,%s),' * int(len(document_list) / 2))[:-1]
                )
                cursor_secondary.execute(
                    final_query, document_list
                )

            document_list = []
            last_document_id = row[0]
        else:
            document_list.extend((new_instance_pk, row[1]))

    if document_list:
        final_query = document_insert_query.format(
            ('(%s,%s),' * int(len(document_list) / 2))[:-1]
        )
        cursor_secondary.execute(
            final_query, document_list
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

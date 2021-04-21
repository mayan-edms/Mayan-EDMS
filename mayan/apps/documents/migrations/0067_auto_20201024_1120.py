from django.db import migrations


def operation_document_file_filename_copy(apps, schema_editor):
    cursor_main = schema_editor.connection.cursor()
    cursor_document_file = schema_editor.connection.cursor()

    query_document_file = '''
        UPDATE {documents_documentfile} SET {filename} = %s WHERE {documents_documentfile}.{id} = %s;
    '''.format(
        documents_documentfile=schema_editor.connection.ops.quote_name('documents_documentfile'),
        filename=schema_editor.connection.ops.quote_name('filename'),
        id=schema_editor.connection.ops.quote_name('id')
    )

    query = '''
        SELECT
            {documents_document}.{label},
            {documents_documentfile}.{id}
        FROM {documents_documentfile}
        INNER JOIN {documents_document} ON (
            {documents_documentfile}.{document_id} = {documents_document}.{id}
        )
    '''.format(
        document_id=schema_editor.connection.ops.quote_name('document_id'),
        documents_document=schema_editor.connection.ops.quote_name('documents_document'),
        documents_documentfile=schema_editor.connection.ops.quote_name('documents_documentfile'),
        id=schema_editor.connection.ops.quote_name('id'),
        label=schema_editor.connection.ops.quote_name('label')
    )

    cursor_main.execute(query)

    for row in cursor_main.fetchall():
        cursor_document_file.execute(
            query_document_file, row
        )


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0066_documentfile_filename'),
    ]

    operations = [
        migrations.RunPython(
            code=operation_document_file_filename_copy,
            reverse_code=migrations.RunPython.noop
        ),
    ]

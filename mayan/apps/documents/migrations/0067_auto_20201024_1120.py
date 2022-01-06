from django.db import models, migrations, reset_queries
from django.db.models import Max
from django.db.models.functions import Concat


def operation_document_file_filename_copy(apps, schema_editor):
    cursor_main = schema_editor.connection.cursor()
    cursor_document_file = schema_editor.connection.cursor()

    query_document_file = '''
        UPDATE {documents_documentfile} SET {filename} = %s WHERE {documents_documentfile}.{id} = %s;
    '''.format(
        documents_documentfile=schema_editor.connection.ops.quote_name(
            name='documents_documentfile'
        ),
        filename=schema_editor.connection.ops.quote_name(name='filename'),
        id=schema_editor.connection.ops.quote_name(name='id')
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
        document_id=schema_editor.connection.ops.quote_name(
            name='document_id'
        ),
        documents_document=schema_editor.connection.ops.quote_name(
            name='documents_document'
        ),
        documents_documentfile=schema_editor.connection.ops.quote_name(
            name='documents_documentfile'
        ),
        id=schema_editor.connection.ops.quote_name(name='id'),
        label=schema_editor.connection.ops.quote_name(name='label')
    )

    cursor_main.execute(query)

    for row in cursor_main.fetchall():
        cursor_document_file.execute(
            query_document_file, row
        )


def operation_set_active_versions(apps, schema_editor):
    Document = apps.get_model(
        app_label='documents', model_name='Document'
    )
    DocumentVersion = apps.get_model(
        app_label='documents', model_name='DocumentVersion'
    )

    cursor_main = schema_editor.connection.create_cursor(name='cursor_main')
    cursor_document_version = schema_editor.connection.cursor()

    # Select the latest version for each document by date.
    document_queryset = Document.objects.only('id').annotate(
        latest_version_timestamp=Max('versions__timestamp')
    )

    # Exclude documents with no latest version.
    document_queryset = document_queryset.exclude(
        latest_version_timestamp=None
    )

    # Create a new unique version identifier.
    document_queryset = document_queryset.annotate(
        version_identifier=Concat(
            'id', 'latest_version_timestamp', output_field=models.CharField()
        )
    )

    # Get all document versions and add a new unique version identifier.
    document_version_queryset = DocumentVersion.objects.only('id').annotate(
        version_identifier=Concat(
            'document_id', 'timestamp', output_field=models.CharField()
        )
    )

    # Set all version as not active.
    DocumentVersion.objects.update(active=False)

    # Workaround MySQL: (1093, "You can't specify target table 'documents_documentversion' for update in FROM clause")
    document_version_queryset = document_version_queryset.filter(
        version_identifier__in=document_queryset.values('version_identifier')
    ).values('id')

    compiler = document_version_queryset.query.get_compiler(
        connection=schema_editor.connection
    )

    cursor_main.execute(
        *document_version_queryset.query.as_sql(
            compiler=compiler, connection=schema_editor.connection
        )
    )

    FETCH_SIZE = 10000
    query_document_version_active_update = '''
        UPDATE {documents_documentversion} SET {active} = '1' WHERE {documents_documentversion}.{id} IN {{}};
    '''.format(
        documents_documentversion=schema_editor.connection.ops.quote_name(
            name='documents_documentversion'
        ),
        active=schema_editor.connection.ops.quote_name(name='active'),
        id=schema_editor.connection.ops.quote_name(name='id')
    )

    while True:
        rows = cursor_main.fetchmany(FETCH_SIZE)
        document_version_values = []

        if not rows:
            break

        for row in rows:
            document_version_values += (row[0],)

        query_argument_placeholders = ('%s',) * len(rows)
        values_query = '({})'.format(', '.join(query_argument_placeholders))
        cursor_document_version.execute(
            query_document_version_active_update.format(values_query), document_version_values
        )
        reset_queries()


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0066_documentfile_filename'),
    ]

    operations = [
        migrations.RunPython(
            code=operation_document_file_filename_copy,
            reverse_code=migrations.RunPython.noop
        ),
        migrations.RunPython(
            code=operation_set_active_versions,
            reverse_code=migrations.RunPython.noop
        ),
    ]

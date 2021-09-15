from django.db import migrations, models, reset_queries
import django.db.models.deletion


def code_remap_document_version_pages_ocr_content(apps, schema_editor):
    """
    The document_page_id field is pointing to the document file page.
    This migration will remap that to point it for the corresponding
    document version page that is connected to the original document file
    page.
    """
    cursor_primary = schema_editor.connection.create_cursor(
        name='merged_content_page_id'
    )
    cursor_secondary = schema_editor.connection.cursor()

    query = '''
        SELECT
            {ocr_documentpageocrcontent}.{content},
            {documents_documentversionpage}.{id}
        FROM {ocr_documentpageocrcontent}
        LEFT OUTER JOIN
            {documents_documentversionpage} ON (
                {documents_documentversionpage}.{object_id} = {ocr_documentpageocrcontent}.{document_page_id}
            )
    '''.format(
        content=schema_editor.connection.ops.quote_name(name='content'),
        document_page_id=schema_editor.connection.ops.quote_name(
            name='document_page_id'
        ),
        documents_documentversionpage=schema_editor.connection.ops.quote_name(
            name='documents_documentversionpage'
        ),
        id=schema_editor.connection.ops.quote_name(name='id'),
        object_id=schema_editor.connection.ops.quote_name(name='object_id'),
        ocr_documentpageocrcontent=schema_editor.connection.ops.quote_name(
            name='ocr_documentpageocrcontent'
        )
    )

    cursor_primary.execute(query)

    insert_query = '''
        INSERT INTO {ocr_documentversionpageocrcontent} (
            content,document_version_page_id
        ) VALUES {{}};
    '''.format(
        ocr_documentversionpageocrcontent=schema_editor.connection.ops.quote_name(
            name='ocr_documentversionpageocrcontent'
        )
    )

    FETCH_SIZE = 10000

    while True:
        rows = cursor_primary.fetchmany(FETCH_SIZE)

        if not rows:
            break

        insert_query_final = insert_query.format(
            ('(%s,%s),' * len(rows))[:-1]
        )

        tuples = []
        for row in rows:
            tuples += row

        cursor_secondary.execute(insert_query_final, tuples)
        reset_queries()


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0075_delete_duplicateddocumentold'),
        ('ocr', '0008_auto_20180917_0646'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentVersionPageOCRContent',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True, primary_key=True,
                        serialize=False, verbose_name='ID'
                    )
                ),
                (
                    'content', models.TextField(
                        blank=True, help_text='The actual text content '
                        'extracted by the OCR backend.',
                        verbose_name='Content'
                    )
                ),
                (
                    'document_version_page', models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='ocr_content',
                        to='documents.DocumentVersionPage',
                        verbose_name='Document version page'
                    )
                ),
            ],
            options={
                'verbose_name': 'Document version page OCR content',
                'verbose_name_plural': 'Document version pages OCR contents',
            },
        ),
        migrations.RunPython(
            code=code_remap_document_version_pages_ocr_content,
            reverse_code=migrations.RunPython.noop
        ),
    ]

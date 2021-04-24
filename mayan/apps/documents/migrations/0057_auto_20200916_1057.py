from django.db import connection, migrations
from django.db.backends.ddl_references import IndexName, Statement, Table
from django.db.migrations.loader import MigrationLoader


def code_drop_btree_index(apps, schema_editor):
    """
    Process BTREE indexes that were not renamed along with their respective
    models.
    """
    index_hashes = ('30bada95', '42757b7a')

    # Access the model from the previous migration to allow deleting the
    # indexes.
    loader = MigrationLoader(connection=connection)
    state = loader.project_state(
        nodes=('documents', '0056_auto_20200916_0959')
    )

    DocumentVersion = state.apps.get_model(
        app_label='documents', model_name='DocumentVersion'
    )
    DocumentVersion._meta.db_table = 'documents_documentfile'

    for index_name in schema_editor._constraint_names(model=DocumentVersion):
        for index_hash in index_hashes:
            if index_hash in index_name:
                if '_fk_' not in index_name:
                    # Index is needed in a foreign key constraint as it
                    # happens with MySQL. Ignore dropping the index.
                    schema_editor.execute(
                        sql=schema_editor._delete_index_sql(
                            model=DocumentVersion, name=index_name
                        )
                    )


def reverse_code_drop_btree_index(apps, schema_editor):
    """
    Create the BTREE indexes that were not renamed along with their
    respective models.
    """
    loader = MigrationLoader(connection=connection)
    state = loader.project_state(
        nodes=('documents', '0056_auto_20200916_0959')
    )

    DocumentVersion = state.apps.get_model(
        app_label='documents', model_name='DocumentVersion'
    )

    field_names = ('document_id', 'timestamp')

    for field_name in field_names:
        fields = (
            DocumentVersion._meta.get_field(field_name=field_name),  # Comma as `fields` is expecting an iterable.
        )

        tablespace_sql = schema_editor._get_index_tablespace_sql(
            model=DocumentVersion, fields=fields, db_tablespace=None
        )

        columns = [field.column for field in fields]
        table = DocumentVersion._meta.db_table

        def create_index_name(*args, **kwargs):
            name = schema_editor._create_index_name(*args, **kwargs)
            return schema_editor.quote_name(name)

        condition = None

        sql = Statement(
            template=schema_editor.sql_create_index,
            table=Table(
                table='documents_documentfile',
                quote_name=schema_editor.quote_name
            ),
            name=IndexName(
                table=table, columns=columns, suffix='',
                create_index_name=create_index_name
            ),
            using='',
            columns=schema_editor._index_columns(
                table=table, columns=columns, col_suffixes=(), opclasses=()
            ),
            extra=tablespace_sql,
            condition=(' WHERE ' + condition) if condition else '',
        )
        schema_editor.execute(sql=sql)


class RunPythonAtomicDynamic(migrations.RunPython):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if connection.features.can_rollback_ddl:
            self.atomic = True
        else:
            self.atomic = False


class Migration(migrations.Migration):
    dependencies = [
        ('documents', '0056_auto_20200916_0959'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DocumentVersion',
            new_name='DocumentFile',
        ),
        RunPythonAtomicDynamic(
            code=code_drop_btree_index,
            reverse_code=reverse_code_drop_btree_index
        ),
        migrations.AlterModelOptions(
            name='documentpageresult',
            options={
                'ordering': (
                    'document_file__document', 'page_number'
                ),
                'verbose_name': 'Document page',
                'verbose_name_plural': 'Document pages'
            },
        ),
        migrations.RenameField(
            model_name='documentpage',
            old_name='document_version',
            new_name='document_file',
        ),
    ]

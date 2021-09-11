from django.db import migrations

from mptt import register

from mayan.apps.templating.classes import Template


def code_rebuild_indexes(apps, schema_editor):
    Document = apps.get_model(
        app_label='documents', model_name='Document'
    )
    IndexTemplate = apps.get_model(
        app_label='document_indexing', model_name='IndexTemplate'
    )
    IndexTemplateNode = apps.get_model(
        app_label='document_indexing', model_name='IndexTemplateNode'
    )
    IndexInstanceNode = apps.get_model(
        app_label='document_indexing', model_name='IndexInstanceNode'
    )

    register(cls=IndexInstanceNode)
    register(cls=IndexTemplateNode)

    def index_document(node_template, document, index_instance_node_parent=None):
        if not index_instance_node_parent:
            index_instance_root_node = node_template.index_instance_nodes.get(parent=None)

            for child in node_template.get_children():
                index_document(
                    node_template=child,
                    document=document,
                    index_instance_node_parent=index_instance_root_node
                )
        elif node_template.enabled:
            try:
                template = Template(
                    template_string=node_template.expression
                )
                result = template.render(
                    context={'document': document}
                )
            except Exception:
                """Templating errors are ignored."""
            else:
                if result:
                    index_instance_node, created = node_template.index_instance_nodes.get_or_create(
                        parent=index_instance_node_parent,
                        value=result
                    )

                    if node_template.link_documents:
                        index_instance_node.documents.add(document)

                    for child in node_template.get_children():
                        index_document(
                            node_template=child,
                            document=document,
                            index_instance_node_parent=index_instance_node
                        )

    for index_template in IndexTemplate.objects.filter(enabled=True):
        index_template_root_node = index_template.node_templates.get(parent=None)

        IndexInstanceNode.objects.create(
            index_template_node=index_template_root_node, parent=None
        )

        for document in Document.objects.filter(document_type__in=index_template.document_types.all()):
            index_document(node_template=index_template_root_node, document=document)


class Migration(migrations.Migration):
    dependencies = [
        ('document_indexing', '0024_auto_20210822_0052'),
    ]

    operations = [
        migrations.RunPython(
            code=code_rebuild_indexes,
            reverse_code=migrations.RunPython.noop
        ),
    ]

from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from .tasks import (
    task_delete_empty, task_index_document, task_remove_document
)


def handler_create_default_document_index(sender, **kwargs):
    DocumentType = apps.get_model(
        app_label='documents', model_name='DocumentType'
    )
    IndexTemplate = apps.get_model(
        app_label='document_indexing', model_name='IndexTemplate'
    )

    index = IndexTemplate.objects.create(
        label=_('Creation date'), slug='creation_date'
    )
    for document_type in DocumentType.objects.all():
        index.document_types.add(document_type)

    root_template_node = index.template_root
    node = root_template_node.get_children().create(
        expression='{{ document.datetime_created|date:"Y" }}', index=index,
        parent=root_template_node
    )
    node.get_children().create(
        expression='{{ document.datetime_created|date:"m" }}',
        index=index, link_documents=True, parent=node
    )


def handler_delete_empty(sender, **kwargs):
    task_delete_empty.apply_async()


def handler_index_document(sender, **kwargs):
    task_index_document.apply_async(
        kwargs=dict(document_id=kwargs['instance'].pk)
    )


def handler_remove_document(sender, **kwargs):
    task_remove_document.apply_async(
        kwargs=dict(document_id=kwargs['instance'].pk)
    )

from __future__ import unicode_literals

import logging

from django.db import models, transaction
from django.template import Context, Template
from django.utils.translation import ugettext_lazy as _

from documents.models import Document

logger = logging.getLogger(__name__)


class DocumentIndexInstanceNodeManager(models.Manager):
    def get_for(self, document):
        return self.filter(documents=document)


class IndexManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class IndexInstanceNodeManager(models.Manager):
    @staticmethod
    def delete_empty_index_nodes_recursive(instance_node):
        """
        Calls itself recursively deleting empty index instance nodes up to
        root
        """

        if instance_node.get_children().count() == 0:
            # if there are no children, delete node and check parent for the
            # same conditions
            parent = instance_node.parent
            if parent:
                instance_node.delete()
                IndexInstanceNodeManager.delete_empty_index_nodes_recursive(
                    parent
                )

    def cascade_eval(self, document, template_node, parent_index_instance=None):
        """
        Evaluate an enabled index expression and update or create all the
        related index instances also recursively calling itself to evaluate
        all the index's children
        """

        if template_node.enabled:
            try:
                template = Template(template_node.expression)
                context = Context({'document': document})
                result = template.render(context=context)
            except Exception as exception:
                error_message = _(
                    'Error indexing document: %(document)s; expression: '
                    '%(expression)s; %(exception)s'
                ) % {
                    'document': document,
                    'expression': template_node.expression,
                    'exception': exception
                }
                logger.debug(error_message)
            else:
                if result:
                    index_instance, created = self.get_or_create(
                        index_template_node=template_node, value=result,
                        parent=parent_index_instance
                    )

                    if template_node.link_documents:
                        index_instance.documents.add(document)

                    for child in template_node.get_children():
                        self.cascade_eval(
                            document=document,
                            template_node=child,
                            parent_index_instance=index_instance
                        )

    def delete_empty_index_nodes(self):
        """
        Delete empty index instance nodes
        """

        for instance_node in self.filter(documents__isnull=True, parent__isnull=False):
            IndexInstanceNodeManager.delete_empty_index_nodes_recursive(
                instance_node
            )

    def index_document(self, document):
        """
        Update or create all the index instances related to a document
        """

        from .models import Index

        with transaction.atomic():
            self.remove_document(document)

            # Only update indexes where the document type is found
            for index in Index.objects.filter(enabled=True, document_types=document.document_type):
                root_instance, created = self.get_or_create(
                    index_template_node=index.template_root, parent=None
                )
                for template_node in index.template_root.get_children():
                    self.cascade_eval(document, template_node, root_instance)

    def remove_document(self, document):
        for index_node in self.filter(documents=document):
            index_node.documents.remove(document)

        self.delete_empty_index_nodes()

    def rebuild_all_indexes(self):
        for instance_node in self.all():
            instance_node.delete()

        for document in Document.objects.all():
            self.index_document(document)

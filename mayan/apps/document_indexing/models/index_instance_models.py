import logging

from django.db import models, transaction
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from mayan.apps.acls.models import AccessControlList
from mayan.apps.documents.models import Document
from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.lock_manager.backends.base import LockingBackend
from mayan.apps.lock_manager.exceptions import LockError
from mayan.apps.templating.classes import Template

from ..managers import (
    DocumentIndexInstanceNodeManager, IndexInstanceManager
)

from .index_template_models import IndexTemplate, IndexTemplateNode

logger = logging.getLogger(name=__name__)


class IndexInstance(IndexTemplate):
    """
    Model that represents an evaluated index. This is an index whose nodes
    have been evaluated against a series of documents. If is a proxy model
    at the moment.
    """
    objects = IndexInstanceManager()

    class Meta:
        proxy = True
        verbose_name = _('Index instance')
        verbose_name_plural = _('Index instances')

    def delete_empty_nodes(self, acquire_lock=True):
        if acquire_lock:
            try:
                if acquire_lock:
                    lock_index_instance = LockingBackend.get_backend().acquire_lock(
                        name=self.get_lock_string()
                    )
            except LockError:
                raise
            else:
                try:
                    return self._delete_empty_nodes()
                finally:
                    lock_index_instance.release()
        else:
            return self._delete_empty_nodes()

    def _delete_empty_nodes(self):
        with transaction.atomic():
            while True:
                queryset = IndexInstanceNode.objects.filter(children=None, index_template_node__link_documents=True, documents=None)
                if queryset.exists():
                    queryset.delete()
                else:
                    break

    def document_add(self, document):
        """
        Method to start the indexing process for a document. The entire process
        happens inside one transaction. The document is first removed from all
        the index nodes to which it already belongs. The different index
        templates that match this document's type are evaluated and for each
        result a node is fetched or created and the document is added to that
        node.
        """
        logger.debug('Index; Indexing document: %s', document)

        index_instance_node_id_list = []

        if Document.valid.filter(pk=document.pk) and self.enabled and self.document_types.filter(pk=document.document_type.pk).exists():
            try:
                locking_backend = LockingBackend.get_backend()

                lock_index_instance = locking_backend.acquire_lock(
                    name=self.get_lock_string()
                )
            except LockError:
                raise
            else:
                try:
                    lock_document = locking_backend.acquire_lock(
                        name=self.get_document_lock_string(document=document)
                    )
                except LockError:
                    raise
                else:
                    try:
                        self.initialize_index_instance_root_node_node()

                        index_instance_node_parent = self.index_instance_root_node

                        index_instance_node_id_list = self._document_add(
                            document=document,
                            index_instance_node_parent=index_instance_node_parent
                        )

                        self.document_remove(
                            acquire_lock=False, document=document,
                            excluded_index_instance_node_id_list=index_instance_node_id_list
                        )
                    finally:
                        lock_document.release()
                finally:
                    lock_index_instance.release()

    def _document_add(self, document, index_instance_node_parent):
        index_instance_node_id_list = []

        for index_template_node in index_instance_node_parent.index_template_node.get_children().filter(enabled=True):
            try:
                template = Template(
                    template_string=index_template_node.expression
                )
                result = template.render(
                    context={'document': document}
                )
            except Exception as exception:
                logger.debug('Evaluating error: %s', exception)
                error_message = _(
                    'Error indexing document: %(document)s; expression: '
                    '%(expression)s; %(exception)s'
                ) % {
                    'document': document,
                    'expression': index_template_node.expression,
                    'exception': exception
                }
                logger.debug(error_message)
            else:
                logger.debug('Evaluation result: %s', result)

                if result:
                    index_instance_node, created = index_template_node.index_instance_nodes.get_or_create(
                        parent=index_instance_node_parent,
                        value=result
                    )
                    index_instance_node_id_list.append(index_instance_node.pk)

                    if index_template_node.link_documents:
                        index_instance_node.documents.add(document)

                    index_instance_node_id_list.extend(
                        self._document_add(
                            document=document,
                            index_instance_node_parent=index_instance_node
                        )
                    )

        return index_instance_node_id_list

    def document_remove(self, document, acquire_lock=True, excluded_index_instance_node_id_list=None):
        excluded_index_instance_node_id_list = excluded_index_instance_node_id_list or ()

        if Document.valid.filter(pk=document.pk) and self.enabled and self.document_types.filter(pk=document.document_type.pk).exists():
            if acquire_lock:
                try:
                    lock_index_instance = LockingBackend.get_backend().acquire_lock(
                        name=self.get_lock_string()
                    )
                except LockError:
                    raise
                else:
                    try:
                        lock_document = LockingBackend.get_backend().acquire_lock(
                            name=self.get_document_lock_string(document=document)
                        )
                    except LockError:
                        raise
                    else:
                        try:
                            return self._document_remove(
                                document=document,
                                excluded_index_instance_node_id_list=excluded_index_instance_node_id_list
                            )
                        finally:
                            lock_document.release()
                    finally:
                        lock_index_instance.release()
            else:
                return self._document_remove(
                    document=document,
                    excluded_index_instance_node_id_list=excluded_index_instance_node_id_list
                )

    def _document_remove(self, document, excluded_index_instance_node_id_list=None):
        excluded_index_instance_node_id_list = excluded_index_instance_node_id_list or ()

        with transaction.atomic():
            document_index_instance_node_queryset = IndexInstanceNode.objects.filter(
                documents=document, index_template_node__index=self
            )
            document_index_instance_node_queryset.exclude(
                pk__in=excluded_index_instance_node_id_list
            ).delete()
            self.delete_empty_nodes(acquire_lock=False)

    def get_absolute_url(self):
        try:
            index_instance_root_node = self.index_instance_root_node
        except IndexInstanceNode.DoesNotExist:
            return '#'
        else:
            return reverse(
                viewname='indexing:index_instance_node_view', kwargs={
                    'index_instance_node_id': index_instance_root_node.pk
                }
            )

    def get_children(self):
        return self.index_instance_root_node.get_children()

    def get_document_lock_string(self, document):
        return 'indexing:document_{}'.format(document.pk)

    def get_descendants(self):
        return self.index_instance_root_node.get_descendants()

    def get_descendants_count(self):
        return self.index_instance_root_node.get_descendants_count()

    get_descendants_count.help_text = _(
        'Total number of nodes with unique values this item contains.'
    )

    def get_descendants_document_count(self, user):
        return self.index_instance_root_node.get_descendants_document_count(
            user=user
        )

    get_descendants_document_count.help_text = _(
        'Total number of unique documents this item contains.'
    )

    def get_lock_string(self):
        return 'indexing:index_instance_{}'.format(self.pk)

    def get_level_count(self):
        return self.index_instance_root_node.get_level_count()

    get_level_count.help_text = _(
        'Total number of node levels this item contains.'
    )

    def get_root(self):
        """Compatibility method."""
        return self.index_instance_root_node

    @property
    def index_instance_root_node(self):
        return self.index_template_root_node.get_index_instance_root_node()

    def initialize_index_instance_root_node_node(self):
        return self.index_template_root_node.initialize_index_instance_root_node()


class IndexInstanceNode(MPTTModel):
    """
    This model represent one instance node from a index template node. That is
    a node template that has been evaluated against a document and the result
    from that evaluation is this node's stored values. Instances of this
    model also point to the original node template.
    """
    parent = TreeForeignKey(
        blank=True, null=True, on_delete=models.CASCADE,
        related_name='children', to='self'
    )
    index_template_node = models.ForeignKey(
        on_delete=models.CASCADE, related_name='index_instance_nodes',
        to=IndexTemplateNode, verbose_name=_('Index template node')
    )
    value = models.CharField(
        blank=True, db_index=True, max_length=128, verbose_name=_('Value')
    )
    documents = models.ManyToManyField(
        related_name='index_instance_nodes', to=Document,
        verbose_name=_('Documents')
    )

    class Meta:
        ordering = ('value',)
        unique_together = ('index_template_node', 'parent', 'value')
        verbose_name = _('Index instance node')
        verbose_name_plural = _('Indexes instances node')

    def __str__(self):
        return self.value

    def get_absolute_url(self):
        return reverse(
            viewname='indexing:index_instance_node_view', kwargs={
                'index_instance_node_id': self.pk
            }
        )

    def get_children_count(self):
        return self.get_children().count()

    def get_descendants_count(self):
        return self.get_descendants().count()

    get_descendants_count.help_text = IndexInstance.get_descendants_count.help_text

    def get_descendants_document_count(self, user):
        queryset = Document.valid.filter(
            index_instance_nodes__in=self.get_descendants(
                include_self=True
            )
        ).distinct()

        return AccessControlList.objects.restrict_queryset(
            permission=permission_document_view,
            queryset=queryset, user=user
        ).count()

    get_descendants_document_count.help_text = IndexInstance.get_descendants_document_count.help_text

    def get_documents(self):
        return Document.valid.filter(pk__in=self.documents.values('pk'))

    def get_full_path(self):
        result = []
        for node in self.get_ancestors(include_self=True):
            if node.is_root_node():
                result.append(force_text(s=self.index()))
            else:
                result.append(force_text(s=node))

        return ' / '.join(result)
    get_full_path.help_text = _(
        'The path to the index including all ancestors.'
    )
    get_full_path.short_description = _('Full path')

    def get_level_count(self):
        return self.get_descendants().values('level').distinct().count()

    get_level_count.help_text = IndexInstance.get_level_count.help_text

    def index(self):
        """
        Return's the index instance of this node instance.
        """
        return IndexInstance.objects.get(pk=self.index_template_node.index.pk)


class DocumentIndexInstanceNode(IndexInstanceNode):
    """
    Proxy model of node instance. It is used to represent the node instance
    in which a document is currently located. It is used to aid in column
    registration. The inherited methods of this model should not be used.
    """
    objects = DocumentIndexInstanceNodeManager()

    class Meta:
        proxy = True
        verbose_name = _('Document index node instance')
        verbose_name_plural = _('Document indexes node instances')


class IndexInstanceNodeSearchResult(IndexInstanceNode):
    class Meta:
        proxy = True
        verbose_name = _('Index instance node')
        verbose_name_plural = _('Index instance nodes')

import logging

from django.db import models, transaction
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.translation import ugettext, ugettext_lazy as _

from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from mayan.apps.acls.models import AccessControlList
from mayan.apps.databases.model_mixins import ExtraDataModelMixin
from mayan.apps.documents.models import Document, DocumentType
from mayan.apps.documents.permissions import permission_document_view
from mayan.apps.events.classes import EventManagerSave
from mayan.apps.events.decorators import method_event
from mayan.apps.lock_manager.backends.base import LockingBackend
from mayan.apps.lock_manager.exceptions import LockError
from mayan.apps.templating.classes import Template

from .events import event_index_template_created, event_index_template_edited
from .managers import (
    DocumentIndexInstanceNodeManager, IndexInstanceManager,
    IndexTemplateManager
)

logger = logging.getLogger(name=__name__)


class IndexTemplate(ExtraDataModelMixin, models.Model):
    """
    Parent model that defines an index and hold all the relationship for its
    template and instance when resolved.
    """
    label = models.CharField(
        help_text=_('Short description of this index.'),
        max_length=128, unique=True, verbose_name=_('Label')
    )
    slug = models.SlugField(
        help_text=_(
            'This value will be used by other apps to reference this index.'
        ), max_length=128, unique=True, verbose_name=_('Slug')
    )
    enabled = models.BooleanField(
        default=True,
        help_text=_(
            'Causes this index to be visible and updated when document data '
            'changes.'
        ),
        verbose_name=_('Enabled')
    )
    document_types = models.ManyToManyField(
        related_name='index_templates', to=DocumentType,
        verbose_name=_('Document types')
    )

    objects = IndexTemplateManager()

    class Meta:
        ordering = ('label',)
        verbose_name = _('Index template')
        verbose_name_plural = _('Index templates')

    def __str__(self):
        return self.label

    def document_types_add(self, queryset, _event_actor=None):
        for document_type in queryset:
            self.document_types.add(document_type)

            event_index_template_edited.commit(
                action_object=document_type,
                actor=_event_actor or self._event_actor, target=self
            )

    def document_types_remove(self, queryset, _event_actor=None):
        for document_type in queryset:
            self.document_types.remove(document_type)

            event_index_template_edited.commit(
                action_object=document_type,
                actor=_event_actor or self._event_actor, target=self
            )

    def delete_index_instance_nodes(self):
        try:
            IndexInstanceNode.objects.filter(index_template_node__index=self).delete()
        except IndexInstanceNode.DoesNotExist:
            """Empty index, ignore this exception."""

    def get_absolute_url(self):
        return reverse(
            viewname='indexing:index_template_view', kwargs={
                'index_template_id': self.pk
            }
        )

    def get_document_types_names(self):
        return ', '.join(
            [
                force_text(s=document_type) for document_type in self.document_types.all()
            ] or ['None']
        )

    @property
    def index_template_root_node(self):
        """
        Return the root node for this index.
        """
        return self.index_template_nodes.get(parent=None)

    def natural_key(self):
        return (self.slug,)

    def rebuild(self):
        """
        Delete and reconstruct the index by deleting of all its instance nodes
        and recreating them for the documents whose types are associated with
        this index
        """
        if self.enabled:
            self.delete_index_instance_nodes()

            # Create the new root index instance node.
            self.index_template_root_node.index_instance_nodes.create()

            index_instance = IndexInstance.objects.get(pk=self.pk)
            index_instance.index_instance_root_node
            # Re-index each document with a type associated with this index.
            for document in Document.objects.filter(document_type__in=self.document_types.all()):
                # Evaluate each index template node for each document
                # associated with this index.
                index_instance.document_add(document=document)

    def reset(self):
        self.delete_index_instance_nodes()

        # Create the new root index instance node.
        self.index_template_root_node.initialize_index_instance_root_node()

    @method_event(
        event_manager_class=EventManagerSave,
        created={
            'event': event_index_template_created,
            'target': 'self',
        },
        edited={
            'event': event_index_template_edited,
            'target': 'self',
        }
    )
    def save(self, *args, **kwargs):
        is_new = not self.pk
        super().save(*args, **kwargs)
        if is_new:
            # Automatically create the root index template node.
            IndexTemplateNode.objects.get_or_create(parent=None, index=self)

        self.index_template_root_node.initialize_index_instance_root_node()


class IndexTemplateNode(MPTTModel):
    """
    The template to generate an index. Each entry represents a level in a
    hierarchy of levels. Each level can contain further levels or a list of
    documents but not both.
    """
    parent = TreeForeignKey(
        blank=True, help_text=_('Parent index template node of this node.'),
        null=True, on_delete=models.CASCADE,
        related_name='children', to='self'
    )
    index = models.ForeignKey(
        on_delete=models.CASCADE, related_name='index_template_nodes',
        to=IndexTemplate, verbose_name=_('Index')
    )
    expression = models.TextField(
        help_text=_(
            'Enter a template to render. Use Django\'s default templating '
            'language.'
        ),
        verbose_name=_('Indexing expression')
    )
    enabled = models.BooleanField(
        default=True,
        help_text=_(
            'Causes this node to be visible and updated when document data '
            'changes.'
        ),
        verbose_name=_('Enabled')
    )
    link_documents = models.BooleanField(
        default=False,
        help_text=_(
            'Check this option to have this node act as a container for '
            'documents and not as a parent for further nodes.'
        ),
        verbose_name=_('Link documents')
    )

    class Meta:
        verbose_name = _('Index template node')
        verbose_name_plural = _('Index template nodes')

    def __str__(self):
        if self.is_root_node():
            return ugettext('Root')
        else:
            return self.expression

    def get_index_instance_root_node(self):
        return self.index_instance_nodes.get(parent=None)

    def initialize_index_instance_root_node(self):
        self.index_instance_nodes.get_or_create(parent=None)


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

                        self.document_remove(acquire_lock=False, document=document)

                        index_instance_node_parent = self.index_instance_root_node

                        self._document_add(document=document, index_instance_node_parent=index_instance_node_parent)
                    finally:
                        lock_document.release()
                finally:
                    lock_index_instance.release()

    def _document_add(self, document, index_instance_node_parent):
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

                    if index_template_node.link_documents:
                        index_instance_node.documents.add(document)

                    self._document_add(document=document, index_instance_node_parent=index_instance_node)

    def document_remove(self, document, acquire_lock=True):
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
                            return self._document_remove(document=document)
                        finally:
                            lock_document.release()
                    finally:
                        lock_index_instance.release()
            else:
                return self._document_remove(document=document)

    def _document_remove(self, document):
        with transaction.atomic():
            document.index_instance_nodes.through._meta.model.objects.filter(document=document, indexinstancenode__index_template_node__index=self).delete()
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

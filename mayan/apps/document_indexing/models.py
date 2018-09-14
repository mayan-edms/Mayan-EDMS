from __future__ import absolute_import, unicode_literals

import logging

from django.db import models, transaction
from django.template import Context, Template
from django.urls import reverse
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.translation import ugettext, ugettext_lazy as _

from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from acls.models import AccessControlList
from documents.models import Document, DocumentType
from documents.permissions import permission_document_view
from lock_manager import LockError
from lock_manager.runtime import locking_backend

from .managers import (
    DocumentIndexInstanceNodeManager, IndexManager, IndexInstanceNodeManager
)

logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class Index(models.Model):
    """
    Parent model that defines an index and hold all the relationship for its
    template and instance when resolved.
    """
    label = models.CharField(
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
        to=DocumentType, verbose_name=_('Document types')
    )

    objects = IndexManager()

    class Meta:
        ordering = ('label',)
        verbose_name = _('Index')
        verbose_name_plural = _('Indexes')

    def __str__(self):
        return self.label

    def get_absolute_url(self):
        try:
            return reverse(
                'indexing:index_instance_node_view',
                args=(self.instance_root.pk,)
            )
        except IndexInstanceNode.DoesNotExist:
            return '#'

    def get_document_types_names(self):
        return ', '.join(
            [
                force_text(document_type) for document_type in self.document_types.all()
            ] or ['None']
        )

    def index_document(self, document):
        logger.debug('Index; Indexing document: %s', document)

        with transaction.atomic():
            # Remove the document from all instance nodes from
            # this index
            for index_instance_node in IndexInstanceNode.objects.filter(index_template_node__index=self, documents=document):
                index_instance_node.remove_document(document=document)

            # Delete all empty nodes. Starting from the bottom up
            for index_instance_node in self.instance_root.get_leafnodes():
                index_instance_node.delete_empty()

        self.template_root.index_document(document=document)

    @property
    def instance_root(self):
        return self.template_root.get_instance_root_node()

    def natural_key(self):
        return (self.slug,)

    def rebuild(self):
        """
        Delete and reconstruct the index by deleting of all its instance nodes
        and recreating them for the documents whose types are associated with
        this index
        """
        # Delete all index instance nodes by deleting the root index
        # instance node. All child index instance nodes will be cascade
        # deleted.
        try:
            self.instance_root.delete()
        except IndexInstanceNode.DoesNotExist:
            # Empty index, ignore this exception
            pass

        # Create the new root index instance node
        self.template_root.index_instance_nodes.create()

        # Re-index each document with a type associated with this index
        for document in Document.objects.filter(document_type__in=self.document_types.all()):
            # Evaluate each index template node for each document
            # associated with this index.
            self.index_document(document=document)

    def save(self, *args, **kwargs):
        """
        Automatically create the root index template node
        """
        super(Index, self).save(*args, **kwargs)
        IndexTemplateNode.objects.get_or_create(parent=None, index=self)

    @property
    def template_root(self):
        return self.node_templates.get(parent=None)


class IndexInstance(Index):
    class Meta:
        proxy = True
        verbose_name = _('Index instance')
        verbose_name_plural = _('Index instances')

    def get_instance_node_count(self):
        try:
            return self.instance_root.get_descendant_count()
        except IndexInstanceNode.DoesNotExist:
            return 0

    def get_item_count(self, user):
        try:
            return self.instance_root.get_item_count(user=user)
        except IndexInstanceNode.DoesNotExist:
            return 0


@python_2_unicode_compatible
class IndexTemplateNode(MPTTModel):
    """
    The template to generate an index. Each entry represents a level in a
    hierarchy of levels. Each level can contain further levels or a list of
    documents but not both.
    """
    parent = TreeForeignKey(
        blank=True, null=True, on_delete=models.CASCADE, to='self',
    )
    index = models.ForeignKey(
        on_delete=models.CASCADE, related_name='node_templates', to=Index,
        verbose_name=_('Index')
    )
    expression = models.TextField(
        help_text=_(
            'Enter a template to render. '
            'Use Django\'s default templating language '
            '(https://docs.djangoproject.com/en/1.11/ref/templates/builtins/)'
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
        verbose_name = _('Index node template')
        verbose_name_plural = _('Indexes node template')

    def __str__(self):
        if self.is_root_node():
            return ugettext('Root')
        else:
            return self.expression

    def get_lock_string(self):
        return 'indexing:indexing_template_node_{}'.format(self.pk)

    def get_instance_root_node(self):
        index_instance_root_node, create = self.index_instance_nodes.get_or_create(parent=None)
        return index_instance_root_node

    def index_document(self, document, acquire_lock=True, index_instance_node_parent=None):
        # Start transaction after the lock in case the locking backend uses
        # the database.
        try:
            if acquire_lock:
                lock = locking_backend.acquire_lock(
                    self.get_lock_string()
                )
        except LockError:
            raise
        else:
            try:
                logger.debug(
                    'IndexTemplateNode; Indexing document: %s', document
                )

                if not index_instance_node_parent:
                    # I'm the root
                    with transaction.atomic():
                        index_instance_root_node = self.get_instance_root_node()

                        for child in self.get_children():
                            child.index_document(
                                document=document, acquire_lock=False,
                                index_instance_node_parent=index_instance_root_node
                            )
                elif self.enabled:
                    with transaction.atomic():
                        logger.debug('IndexTemplateNode; non parent: evaluating')
                        logger.debug('My parent template is: %s', self.parent)
                        logger.debug(
                            'My parent instance node is: %s',
                            index_instance_node_parent
                        )
                        logger.debug(
                            'IndexTemplateNode; Evaluating template: %s', self.expression
                        )

                        try:
                            context = Context({'document': document})
                            template = Template(self.expression)
                            result = template.render(context=context)
                        except Exception as exception:
                            logger.debug('Evaluating error: %s', exception)
                            error_message = _(
                                'Error indexing document: %(document)s; expression: '
                                '%(expression)s; %(exception)s'
                            ) % {
                                'document': document,
                                'expression': self.expression,
                                'exception': exception
                            }
                            logger.debug(error_message)
                        else:
                            logger.debug('Evaluation result: %s', result)

                            if result:
                                index_instance_node, created = self.index_instance_nodes.get_or_create(
                                    parent=index_instance_node_parent,
                                    value=result
                                )

                                if self.link_documents:
                                    index_instance_node.documents.add(document)

                                for child in self.get_children():
                                    child.index_document(
                                        document=document, acquire_lock=False,
                                        index_instance_node_parent=index_instance_node
                                    )
            finally:
                if acquire_lock:
                    lock.release()


@python_2_unicode_compatible
class IndexInstanceNode(MPTTModel):
    parent = TreeForeignKey(
        blank=True, null=True, on_delete=models.CASCADE, to='self',
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

    objects = IndexInstanceNodeManager()

    class Meta:
        verbose_name = _('Index node instance')
        verbose_name_plural = _('Indexes node instances')

    def __str__(self):
        return self.value

    def delete_empty(self):
        # Prevent another process to delete this node.
        try:
            lock = locking_backend.acquire_lock(
                self.index_template_node.get_lock_string()
            )
        except LockError:
            raise
        else:
            try:
                if self.documents.count() == 0 and self.get_children().count() == 0:
                    if not self.is_root_node():
                        # I'm not a root node, I can be deleted
                        self.delete()

                        if self.parent.is_root_node():
                            # My parent is not a root node, it can be deleted
                            self.parent.delete_empty()
            finally:
                lock.release()

    def get_absolute_url(self):
        return reverse('indexing:index_instance_node_view', args=(self.pk,))

    def get_children_count(self):
        return self.get_children().count()

    def get_descendants_count(self):
        return self.get_descendants().count()

    def get_descendants_document_count(self, user):
        return AccessControlList.objects.filter_by_access(
            permission=permission_document_view, user=user,
            queryset=Document.objects.filter(
                index_instance_nodes__in=self.get_descendants(
                    include_self=True
                )
            )
        ).count()

    def get_full_path(self):
        result = []
        for node in self.get_ancestors(include_self=True):
            if node.is_root_node():
                result.append(force_text(self.index()))
            else:
                result.append(force_text(node))

        return ' / '.join(result)

    def get_item_count(self, user):
        if self.index_template_node.link_documents:
            queryset = AccessControlList.objects.filter_by_access(
                permission_document_view, user, queryset=self.documents
            )

            return queryset.count()
        else:
            return self.get_children().count()

    def get_lock_string(self):
        return 'indexing:index_instance_node_{}'.format(self.pk)

    def index(self):
        return IndexInstance.objects.get(pk=self.index_template_node.index.pk)

    def remove_document(self, document):
        """
        The argument `acquire_lock` controls whether or not this method
        acquires or lock. The case for this is to acquire when called directly
        or not to acquire when called as part of a larger index process
        that already has a lock
        """
        # Prevent another process to work on this node. We use the node's
        # parent template node for the lock
        try:
            lock = locking_backend.acquire_lock(
                self.index_template_node.get_lock_string()
            )
        except LockError:
            raise
        else:
            try:
                self.documents.remove(document)
            finally:
                lock.release()


class DocumentIndexInstanceNode(IndexInstanceNode):
    objects = DocumentIndexInstanceNodeManager()

    class Meta:
        proxy = True
        verbose_name = _('Document index node instance')
        verbose_name_plural = _('Document indexes node instances')

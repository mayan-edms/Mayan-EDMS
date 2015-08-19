from __future__ import absolute_import, unicode_literals

from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext, ugettext_lazy as _

from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from acls.models import AccessControlList
from documents.models import Document, DocumentType
from documents.permissions import permission_document_view
from permissions import Permission

from .managers import IndexManager, IndexInstanceNodeManager


@python_2_unicode_compatible
class Index(models.Model):
    label = models.CharField(
        max_length=128, unique=True, verbose_name=_('Label')
    )
    slug = models.SlugField(
        help_text=_(
            'This values will be used by other apps to reference this index.'
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
        DocumentType, verbose_name=_('Document types')
    )

    objects = IndexManager()

    @property
    def template_root(self):
        return self.node_templates.get(parent=None)

    @property
    def instance_root(self):
        return self.template_root.node_instance.get()

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

    def save(self, *args, **kwargs):
        """
        Automatically create the root index template node
        """

        super(Index, self).save(*args, **kwargs)
        IndexTemplateNode.objects.get_or_create(parent=None, index=self)

    def get_document_types_names(self):
        return ', '.join(
            [
                unicode(document_type) for document_type in self.document_types.all()
            ] or ['None']
        )

    class Meta:
        verbose_name = _('Index')
        verbose_name_plural = _('Indexes')


class IndexInstance(Index):
    def get_instance_node_count(self):
        try:
            return self.instance_root.get_descendant_count()
        except IndexInstanceNode.DoesNotExist:
            return 0

    def get_items_count(self, user):
        try:
            return self.instance_root.get_item_count(user=user)
        except IndexInstanceNode.DoesNotExist:
            return 0

    class Meta:
        proxy = True
        verbose_name = _('Index instance')
        verbose_name_plural = _('Index instances')


@python_2_unicode_compatible
class IndexTemplateNode(MPTTModel):
    parent = TreeForeignKey('self', blank=True, null=True)
    index = models.ForeignKey(
        Index, related_name='node_templates', verbose_name=_('Index')
    )
    expression = models.CharField(
        max_length=128,
        help_text=_(
            'Enter a template to render. '
            'Use Django\'s default templating language '
            '(https://docs.djangoproject.com/en/1.7/ref/templates/builtins/)'
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

    def __str__(self):
        if self.is_root_node():
            return ugettext('<%s Root>') % self.index
        else:
            return self.expression

    class Meta:
        verbose_name = _('Index node template')
        verbose_name_plural = _('Indexes node template')


@python_2_unicode_compatible
class IndexInstanceNode(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True)
    index_template_node = models.ForeignKey(
        IndexTemplateNode, related_name='node_instance',
        verbose_name=_('Index template node')
    )
    value = models.CharField(
        blank=True, db_index=True, max_length=128, verbose_name=_('Value')
    )
    documents = models.ManyToManyField(
        Document, related_name='node_instances', verbose_name=_('Documents')
    )

    objects = IndexInstanceNodeManager()

    def __str__(self):
        return self.value

    def get_absolute_url(self):
        return reverse('indexing:index_instance_node_view', args=(self.pk,))

    @property
    def children(self):
        # Convenience method for serializer
        return self.get_children()

    def index(self):
        return self.index_template_node.index

    def get_item_count(self, user):
        if self.index_template_node.link_documents:
            queryset = self.documents

            try:
                Permission.check_permissions(user, (permission_document_view,))
            except PermissionDenied:
                queryset = AccessControlList.objects.filter_by_access(
                    permission_document_view, user, queryset
                )

            return queryset.count()
        else:
            return self.get_children().count()

    class Meta:
        verbose_name = _('Index node instance')
        verbose_name_plural = _('Indexes node instances')


class DocumentIndexInstanceNodeManager(models.Manager):
    def get_for(self, document):
        return self.filter(documents=document)


class DocumentIndexInstanceNode(IndexInstanceNode):
    objects = DocumentIndexInstanceNodeManager()

    class Meta:
        proxy = True
        verbose_name = _('Document index node instance')
        verbose_name_plural = _('Document indexes node instances')

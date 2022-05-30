import logging

from django.apps import apps
from django.db import models
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.translation import ugettext, ugettext_lazy as _

from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from mayan.apps.databases.model_mixins import ExtraDataModelMixin
from mayan.apps.documents.models import Document, DocumentType
from mayan.apps.events.classes import (
    EventManagerMethodAfter, EventManagerSave, ModelEventType
)
from mayan.apps.events.decorators import method_event
from mayan.apps.events.models import StoredEventType

from ..events import (
    event_index_template_created, event_index_template_edited
)
from ..managers import IndexTemplateManager

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

    def do_event_triggers_populate(self):
        entries = []

        for event_type in ModelEventType.get_for_class(klass=Document):
            entries.append(
                IndexTemplateEventTrigger(
                    index_template=self,
                    stored_event_type=event_type.get_stored_event_type()
                )
            )

        IndexTemplateEventTrigger.objects.bulk_create(entries)

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
        IndexInstanceNode = apps.get_model(
            app_label='document_indexing', model_name='IndexInstanceNode'
        )

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
        IndexInstance = apps.get_model(
            app_label='document_indexing', model_name='IndexInstance'
        )

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
            self.do_event_triggers_populate()

        self.index_template_root_node.initialize_index_instance_root_node()


class IndexTemplateEventTrigger(ExtraDataModelMixin, models.Model):
    index_template = models.ForeignKey(
        on_delete=models.CASCADE, related_name='event_triggers',
        to=IndexTemplate, verbose_name=_('Index template')
    )
    stored_event_type = models.ForeignKey(
        on_delete=models.CASCADE, to=StoredEventType,
        verbose_name=_('Event type')
    )

    class Meta:
        unique_together = ('index_template', 'stored_event_type')
        verbose_name = _('Index template event trigger')
        verbose_name_plural = _('Index template event triggers')

    def __str__(self):
        return str(self.stored_event_type)

    @method_event(
        event_manager_class=EventManagerMethodAfter,
        event=event_index_template_edited,
        target='index_template'
    )
    def delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs)

    @method_event(
        event_manager_class=EventManagerSave,
        created={
            'event': event_index_template_edited,
            'target': 'index_template'
        },
        edited={
            'event': event_index_template_edited,
            'target': 'index_template'
        }
    )
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


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

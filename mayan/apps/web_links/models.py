from django.db import models
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from mayan.apps.databases.model_mixins import ExtraDataModelMixin
from mayan.apps.documents.models import DocumentType
from mayan.apps.events.classes import EventManagerSave
from mayan.apps.events.decorators import method_event
from mayan.apps.templating.classes import Template

from .events import (
    event_web_link_created, event_web_link_edited, event_web_link_navigated
)
from .managers import WebLinkManager


class WebLink(ExtraDataModelMixin, models.Model):
    """
    This model stores the basic fields for a web link. Web links allow
    generating links from documents to external resources.
    """
    label = models.CharField(
        db_index=True, help_text=_('A short text describing the web link.'),
        max_length=96, unique=True, verbose_name=_('Label')
    )
    template = models.TextField(
        help_text=_(
            'Template that will be used to craft the final URL of the '
            'web link.'
        ), verbose_name=_('Template')
    )
    enabled = models.BooleanField(default=True, verbose_name=_('Enabled'))
    document_types = models.ManyToManyField(
        related_name='web_links', to=DocumentType,
        verbose_name=_('Document types')
    )

    class Meta:
        ordering = ('label',)
        verbose_name = _('Web link')
        verbose_name_plural = _('Web links')

    def __str__(self):
        return self.label

    def document_types_add(self, queryset, _event_actor=None):
        for document_type in queryset:
            self.document_types.add(document_type)
            event_web_link_edited.commit(
                action_object=document_type,
                actor=_event_actor or self._event_actor, target=self
            )

    def document_types_remove(self, queryset, _event_actor=None):
        for document_type in queryset:
            self.document_types.remove(document_type)
            event_web_link_edited.commit(
                action_object=document_type,
                actor=_event_actor or self._event_actor, target=self
            )

    def get_absolute_url(self):
        return reverse(
            viewname='web_links:web_link_edit', kwargs={
                'web_link_id': self.pk
            }
        )

    @method_event(
        event_manager_class=EventManagerSave,
        created={
            'event': event_web_link_created,
            'target': 'self',
        },
        edited={
            'event': event_web_link_edited,
            'target': 'self',
        }
    )
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class ResolvedWebLink(WebLink):
    """
    Proxy model to represent an already resolved web link. Used for easier
    colums registration.
    """
    objects = WebLinkManager()

    class Meta:
        proxy = True

    def get_redirect(self, document, user):
        event_web_link_navigated.commit(
            actor=user, action_object=document,
            target=self
        )
        return HttpResponseRedirect(
            redirect_to=self.get_redirect_url_for(document=document)
        )

    def get_redirect_url_for(self, document):
        return Template(template_string=self.template).render(
            context={'document': document}
        )

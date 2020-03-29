from django.db import models, transaction
from django.template import Context, Template
from django.urls import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.events import event_document_type_edited
from mayan.apps.documents.models import DocumentType

from .events import event_web_link_created, event_web_link_edited
from .managers import WebLinkManager


@python_2_unicode_compatible
class WebLink(models.Model):
    """
    This model stores the basic fields for a web link. Web links allow
    generating links from documents to external resources.
    """
    label = models.CharField(
        db_index=True, help_text=_('A short text describing the web link.'),
        max_length=96, verbose_name=_('Label')
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

    objects = WebLinkManager()

    class Meta:
        ordering = ('label',)
        verbose_name = _('Web link')
        verbose_name_plural = _('Web links')

    def __str__(self):
        return self.label

    def document_types_add(self, queryset, _user=None):
        with transaction.atomic():
            event_web_link_edited.commit(
                actor=_user, target=self
            )
            for obj in queryset:
                self.document_types.add(obj)
                event_document_type_edited.commit(
                    actor=_user, action_object=self, target=obj
                )

    def document_types_remove(self, queryset, _user=None):
        with transaction.atomic():
            event_web_link_edited.commit(
                actor=_user, target=self
            )
            for obj in queryset:
                self.document_types.remove(obj)
                event_document_type_edited.commit(
                    actor=_user, action_object=self, target=obj
                )

    def get_absolute_url(self):
        return reverse(
            viewname='web_links:web_link_edit', kwargs={
                'web_link_id': self.pk
            }
        )

    def save(self, *args, **kwargs):
        _user = kwargs.pop('_user', None)

        with transaction.atomic():
            is_new = not self.pk
            super(WebLink, self).save(*args, **kwargs)
            if is_new:
                event_web_link_created.commit(
                    actor=_user, target=self
                )
            else:
                event_web_link_edited.commit(
                    actor=_user, target=self
                )


class ResolvedWebLink(WebLink):
    """
    Proxy model to represent an already resolved web link. Used for easier
    colums registration.
    """
    class Meta:
        proxy = True

    def get_url_for(self, document):
        context = Context({'document': document})

        return Template(self.template).render(context=context)

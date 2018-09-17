from __future__ import absolute_import, unicode_literals

from django.db import models
from django.urls import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from colorful.fields import RGBColorField

from acls.models import AccessControlList
from documents.models import Document
from documents.permissions import permission_document_view

from .events import (
    event_tag_attach, event_tag_created, event_tag_edited, event_tag_remove
)
from .widgets import widget_single_tag


@python_2_unicode_compatible
class Tag(models.Model):
    label = models.CharField(
        db_index=True, help_text=_(
            'A short text used as the tag name.'
        ), max_length=128, unique=True, verbose_name=_('Label')
    )
    color = RGBColorField(
        help_text=_('The RGB color values for the tag.'),
        verbose_name=_('Color')
    )
    documents = models.ManyToManyField(
        related_name='tags', to=Document, verbose_name=_('Documents')
    )

    class Meta:
        ordering = ('label',)
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

    def __str__(self):
        return self.label

    def attach_to(self, document, user=None):
        self.documents.add(document)
        event_tag_attach.commit(
            action_object=self, actor=user, target=document
        )

    def get_absolute_url(self):
        return reverse('tags:tag_tagged_item_list', args=(str(self.pk),))

    def get_document_count(self, user):
        queryset = AccessControlList.objects.filter_by_access(
            permission_document_view, user, queryset=self.documents
        )

        return queryset.count()

    def get_preview_widget(self):
        return widget_single_tag(tag=self)
    get_preview_widget.short_description = _('Preview')

    def remove_from(self, document, user=None):
        self.documents.remove(document)
        event_tag_remove.commit(
            action_object=self, actor=user, target=document
        )

    def save(self, *args, **kwargs):
        user = kwargs.pop('_user', None)
        created = not self.pk

        result = super(Tag, self).save(*args, **kwargs)

        if created:
            event_tag_created.commit(actor=user, target=self)
        else:
            event_tag_edited.commit(actor=user, target=self)

        return result


class DocumentTag(Tag):
    class Meta:
        proxy = True
        verbose_name = _('Document tag')
        verbose_name_plural = _('Document tags')

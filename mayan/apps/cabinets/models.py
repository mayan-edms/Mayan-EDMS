from __future__ import absolute_import, unicode_literals

from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.db import connection, models, transaction
from django.urls import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from mayan.apps.acls.models import AccessControlList
from mayan.apps.documents.models import Document
from mayan.apps.documents.permissions import permission_document_view

from .events import (
    event_cabinet_created, event_cabinet_edited, event_cabinet_add_document,
    event_cabinet_remove_document
)
from .search import cabinet_search  # NOQA


@python_2_unicode_compatible
class Cabinet(MPTTModel):
    """
    Model to store a hierarchical tree of document containers. Each container
    can store an unlimited number of documents using an M2M field. Only
    the top level container is can have an ACL. All child container's
    access is delegated to their corresponding root container.
    """
    parent = TreeForeignKey(
        blank=True, db_index=True, null=True, on_delete=models.CASCADE,
        related_name='children', to='self'
    )
    label = models.CharField(
        help_text=_('A short text used to identify the cabinet.'),
        max_length=128, verbose_name=_('Label')
    )
    documents = models.ManyToManyField(
        blank=True, related_name='cabinets', to=Document,
        verbose_name=_('Documents')
    )

    class Meta:
        ordering = ('parent__label', 'label')
        # unique_together doesn't work if there is a FK
        # https://code.djangoproject.com/ticket/1751
        unique_together = ('parent', 'label')
        verbose_name = _('Cabinet')
        verbose_name_plural = _('Cabinets')

    def __str__(self):
        return self.get_full_path()

    def document_add(self, document, _user=None):
        """
        Add a document to a container. This can be done without using this
        method but this method provides the event commit already coded.
        """
        with transaction.atomic():
            self.documents.add(document)
            event_cabinet_add_document.commit(
                action_object=self, actor=_user, target=document
            )

    def document_remove(self, document, _user=None):
        """
        Remove a document from a cabinet. This method provides the
        corresponding event commit.
        """
        with transaction.atomic():
            self.documents.remove(document)
            event_cabinet_remove_document.commit(
                action_object=self, actor=_user, target=document
            )

    def get_absolute_url(self):
        return reverse(viewname='cabinets:cabinet_view', kwargs={'pk': self.pk})

    def get_document_count(self, user):
        """
        Return numeric count of the total documents in a cabinet. The count
        is filtered by access.
        """
        return self.get_documents_queryset(user=user).count()

    def get_documents_queryset(self, user):
        """
        Provide a queryset of the documents in a cabinet. The queryset is
        filtered by access.
        """
        return AccessControlList.objects.restrict_queryset(
            permission=permission_document_view, queryset=self.documents,
            user=user
        )

    def get_full_path(self):
        """
        Returns a string that represents the path to the cabinet. The
        path string starts from the root cabinet.
        """
        result = []
        for node in self.get_ancestors(include_self=True):
            result.append(node.label)

        return ' / '.join(result)

    def save(self, *args, **kwargs):
        _user = kwargs.pop('_user', None)

        with transaction.atomic():
            is_new = not self.pk
            super(Cabinet, self).save(*args, **kwargs)
            if is_new:
                event_cabinet_created.commit(
                    actor=_user, target=self
                )
            else:
                event_cabinet_edited.commit(
                    actor=_user, target=self
                )

    def validate_unique(self, exclude=None):
        """
        Explicit validation of uniqueness of parent+label as the provided
        unique_together check in Meta is not working for all 100% cases
        when there is a FK in the unique_together tuple
        https://code.djangoproject.com/ticket/1751
        """
        with transaction.atomic():
            if connection.vendor == 'oracle':
                queryset = Cabinet.objects.filter(parent=self.parent, label=self.label)
            else:
                queryset = Cabinet.objects.select_for_update().filter(parent=self.parent, label=self.label)

            if queryset.exists():
                params = {
                    'model_name': _('Cabinet'),
                    'field_labels': _('Parent and Label')
                }
                raise ValidationError(
                    {
                        NON_FIELD_ERRORS: [
                            ValidationError(
                                message=_(
                                    '%(model_name)s with this %(field_labels)s already '
                                    'exists.'
                                ), code='unique_together', params=params,
                            )
                        ],
                    },
                )


class DocumentCabinet(Cabinet):
    """
    Represent a document's cabinet. This Model is a proxy model from Cabinet
    and is used as an alias to map columns to it without having to map them
    to the base Cabinet model.
    """
    class Meta:
        proxy = True
        verbose_name = _('Document cabinet')
        verbose_name_plural = _('Document cabinets')

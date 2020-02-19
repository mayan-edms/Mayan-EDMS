from __future__ import unicode_literals

from django.apps import apps
from django.db import transaction
from django.utils.translation import ugettext_lazy as _

from .events import event_tag_attach, event_tag_remove


def method_document_tags_attach(self, queryset, _user=None):
    """
    Attach a document to a tag and commit the corresponding event.
    """
    with transaction.atomic():
        for tag in queryset:
            self.tags.add(tag)
            event_tag_attach.commit(
                action_object=tag, actor=_user, target=self
            )


def method_document_get_tags(self, permission, user):
    AccessControlList = apps.get_model(
        app_label='acls', model_name='AccessControlList'
    )
    DocumentTag = apps.get_model(app_label='tags', model_name='DocumentTag')

    return AccessControlList.objects.restrict_queryset(
        permission=permission,
        queryset=DocumentTag.objects.filter(documents=self), user=user
    )


method_document_get_tags.help_text = _(
    'Return a the tags attached to the document.'
)
method_document_get_tags.short_description = _('get_tags()')


def method_document_tags_remove(self, queryset, _user=None):
    """
    Remove a document from a tag and commit the corresponding event.
    """
    with transaction.atomic():
        for tag in queryset:
            self.tags.remove(tag)
            event_tag_remove.commit(
                action_object=tag, actor=_user, target=self
            )

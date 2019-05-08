from __future__ import unicode_literals

from django.apps import apps
from django.utils.translation import ugettext_lazy as _


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

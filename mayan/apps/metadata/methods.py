from django.apps import apps
from django.utils.translation import ugettext_lazy as _


def method_document_get_metadata(self, permission, user):
    AccessControlList = apps.get_model(
        app_label='acls', model_name='AccessControlList'
    )
    DocumentMetadata = apps.get_model(
        app_label='metadata', model_name='DocumentMetadata'
    )

    return AccessControlList.objects.restrict_queryset(
        permission=permission,
        queryset=DocumentMetadata.objects.filter(document=self), user=user
    )


method_document_get_metadata.help_text = _(
    'Return the metadata of the document.'
)
method_document_get_metadata.short_description = 'get_metadata()'

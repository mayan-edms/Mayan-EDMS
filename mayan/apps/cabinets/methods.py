from django.apps import apps
from django.utils.translation import ugettext_lazy as _


def method_document_get_cabinets(self, permission, user):
    AccessControlList = apps.get_model(
        app_label='acls', model_name='AccessControlList'
    )
    DocumentCabinet = apps.get_model(
        app_label='cabinets', model_name='DocumentCabinet'
    )

    return AccessControlList.objects.restrict_queryset(
        permission=permission,
        queryset=DocumentCabinet.objects.filter(documents=self), user=user
    )


method_document_get_cabinets.help_text = _(
    'Return a list of cabinets containing the document.'
)
method_document_get_cabinets.short_description = _('get_cabinets()')

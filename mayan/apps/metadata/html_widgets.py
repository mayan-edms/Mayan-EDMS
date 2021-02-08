from django.apps import apps

from mayan.apps.common.utils import resolve_attribute
from mayan.apps.navigation.html_widgets import SourceColumnWidget

from .permissions import permission_document_metadata_view


class DocumentMetadataWidget(SourceColumnWidget):
    """
    A widget that displays the metadata for the given document or related
    object.
    """
    template_name = 'metadata/document_metadata_widget.html'

    def __init__(self, attribute=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attribute = attribute

    def get_extra_context(self):
        AccessControlList = apps.get_model(
            app_label='acls', model_name='AccessControlList'
        )

        if self.attribute:
            attribute = resolve_attribute(
                obj=self.value, attribute=self.attribute
            )
        else:
            attribute = self.value

        queryset = AccessControlList.objects.restrict_queryset(
            queryset=attribute.metadata.all(),
            permission=permission_document_metadata_view,
            user=self.request.user
        )

        return {'queryset': queryset}

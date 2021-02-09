from django.apps import apps
from django.core.exceptions import PermissionDenied

from mayan.apps.navigation.html_widgets import SourceColumnWidget

from .permissions import permission_cabinet_view


class DocumentCabinetWidget(SourceColumnWidget):
    """
    A widget that displays the cabinets containing the given document.
    """
    template_name = 'cabinets/document_cabinets_widget.html'

    def get_extra_context(self):
        AccessControlList = apps.get_model(
            app_label='acls', model_name='AccessControlList'
        )

        try:
            AccessControlList.objects.check_access(
                obj=self.value,
                permissions=(permission_cabinet_view,),
                user=self.request.user
            )
        except PermissionDenied:
            queryset = self.value.cabinets.none()
        else:
            queryset = self.value.get_cabinets(
                permission=permission_cabinet_view,
                user=self.request.user
            )

        return {'cabinets': queryset}

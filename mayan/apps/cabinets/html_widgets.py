from mayan.apps.navigation.html_widgets import SourceColumnWidget

from .permissions import permission_cabinet_view


class DocumentCabinetWidget(SourceColumnWidget):
    template_name = 'cabinets/document_cabinets_widget.html'

    def get_extra_context(self):
        return {
            'cabinets': self.value.get_cabinets(
                permission=permission_cabinet_view, user=self.request.user
            )
        }

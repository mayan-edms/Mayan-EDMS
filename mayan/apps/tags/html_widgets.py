from django.apps import apps
from django.core.exceptions import PermissionDenied
from django.template.loader import render_to_string

from mayan.apps.navigation.html_widgets import SourceColumnWidget

from .permissions import permission_tag_view


class DocumentTagWidget(SourceColumnWidget):
    """
    A tag widget that displays the tags for the given document.
    """
    template_name = 'tags/document_tags_widget.html'

    def get_extra_context(self):
        AccessControlList = apps.get_model(
            app_label='acls', model_name='AccessControlList'
        )

        try:
            AccessControlList.objects.check_access(
                obj=self.value,
                permissions=(permission_tag_view,),
                user=self.request.user
            )
        except PermissionDenied:
            queryset = self.value.tags.none()
        else:
            queryset = self.value.get_tags(
                permission=permission_tag_view,
                user=self.request.user
            )

        return {'tags': queryset}


def widget_single_tag(tag):
    return render_to_string(
        template_name='tags/tag_widget.html', context={'tag': tag}
    )

from django.utils.safestring import mark_safe

from mayan.apps.converter.transformations import TransformationResize
from mayan.apps.navigation.html_widgets import SourceColumnWidget

from .settings import setting_thumbnail_height, setting_thumbnail_width


class ThumbnailWidget(SourceColumnWidget):
    template_name = 'documents/widgets/thumbnail.html'

    def disable_condition(self, instance):
        return instance.is_in_trash

    def get_extra_context(self):
        transformation_instance_list = (
            TransformationResize(
                width=setting_thumbnail_width.value,
                height=setting_thumbnail_height.value
            ),
        )

        return {
            # Disable the clickable link if the document is in the trash
            'disable_title_link': self.disable_condition(instance=self.value),
            'gallery_name': 'document_list',
            'instance': self.value,
            'transformation_instance_list': transformation_instance_list
        }


def document_link(document):
    return mark_safe('<a href="%s">%s</a>' % (
        document.get_absolute_url(), document)
    )

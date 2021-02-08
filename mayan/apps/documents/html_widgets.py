from django.utils.safestring import mark_safe

from mayan.apps.navigation.html_widgets import SourceColumnWidget

from .settings import (
    setting_preview_width, setting_preview_height, setting_thumbnail_width,
    setting_thumbnail_height
)


class ThumbnailWidget(SourceColumnWidget):
    template_name = 'documents/widgets/thumbnail.html'

    def get_extra_context(self):
        return {
            # Disable the clickable link if the document is in the trash
            'disable_title_link': self.value.is_in_trash,
            'gallery_name': 'document_list',
            'instance': self.value,
            'size_preview_width': setting_preview_width.value,
            'size_preview_height': setting_preview_height.value,
            'size_thumbnail_width': setting_thumbnail_width.value,
            'size_thumbnail_height': setting_thumbnail_height.value,
        }


def document_link(document):
    return mark_safe('<a href="%s">%s</a>' % (
        document.get_absolute_url(), document)
    )

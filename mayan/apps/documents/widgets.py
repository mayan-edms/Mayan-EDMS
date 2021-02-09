from django import forms
from django.template.loader import render_to_string

from .settings import (
    setting_display_width, setting_display_height, setting_preview_width,
    setting_preview_height, setting_thumbnail_width, setting_thumbnail_height
)


class CarouselWidget(forms.widgets.Widget):
    """
    Display many small representations of pages
    """
    template_name = 'documents/forms/widgets/page_carousel.html'
    target_view = None

    def __init__(self, attrs=None):
        default_attrs = {
            'height': setting_preview_height.value,
            'width': setting_preview_width.value,
            'target_view': self.target_view
        }

        if attrs:
            default_attrs.update(attrs)

        super().__init__(default_attrs)

    def format_value(self, value):
        if value == '' or value is None:
            return None
        return value


class DocumentFilePagesCarouselWidget(CarouselWidget):
    target_view = 'documents:document_file_page_view'


class ThumbnailFormWidget(forms.widgets.Widget):
    def render(self, *args, **kwargs):
        instance = kwargs['value']
        if instance:
            context = {
                # Disable the clickable link if the document is in the trash
                'disable_title_link': instance.is_in_trash,
                'gallery_name': 'document_list',
                'instance': instance,
                'size_preview_width': setting_preview_width.value,
                'size_preview_height': setting_preview_height.value,
                'size_thumbnail_width': setting_thumbnail_width.value,
                'size_thumbnail_height': setting_thumbnail_height.value,
            }
        else:
            context = {}
        return render_to_string(
            template_name='documents/widgets/thumbnail.html',
            context=context
        )


class DocumentVersionPagesCarouselWidget(CarouselWidget):
    target_view = 'documents:document_version_page_view'


class PageImageWidget(forms.widgets.Widget):
    template_name = 'documents/forms/widgets/page_image_interactive.html'

    def __init__(self, attrs=None):
        default_attrs = {
            'rotation': 0,
            'zoom': 100,
            'width': setting_display_width.value,
            'height': setting_display_height.value,
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

    def format_value(self, value):
        if value == '' or value is None:
            return None
        return value

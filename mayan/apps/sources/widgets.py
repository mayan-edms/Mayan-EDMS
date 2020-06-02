from django.template.loader import render_to_string

from mayan.apps.documents.settings import (
    setting_preview_width, setting_preview_height, setting_thumbnail_width,
    setting_thumbnail_height
)


class StagingFileThumbnailWidget:
    def render(self, instance):
        return render_to_string(
            template_name='documents/widgets/document_thumbnail.html',
            context={
                'container_class': 'staging-file-thumbnail-container',
                'disable_title_link': True,
                'gallery_name': 'sources:staging_list',
                'instance': instance,
                'size_preview_width': setting_preview_width.value,
                'size_preview_height': setting_preview_height.value,
                'size_thumbnail_width': setting_thumbnail_width.value,
                'size_thumbnail_height': setting_thumbnail_height.value,
            }
        )

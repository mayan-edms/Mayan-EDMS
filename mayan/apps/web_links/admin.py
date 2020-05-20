from django.contrib import admin
from .models import WebLink


@admin.register(WebLink)
class WebLinkAdmin(admin.ModelAdmin):
    def document_type_list(self, instance):
        return ','.join(
            instance.document_types.values_list('label', flat=True)
        )

    filter_horizontal = ('document_types',)
    list_display = ('label', 'template', 'enabled', 'document_type_list')

from django.contrib import admin

from .models import (
    DocumentFileOCRError, DocumentPageOCRContent, DocumentTypeSettings
)


@admin.register(DocumentPageOCRContent)
class DocumentPageOCRContentAdmin(admin.ModelAdmin):
    list_display = ('document_page',)


@admin.register(DocumentTypeSettings)
class DocumentTypeSettingsAdmin(admin.ModelAdmin):
    list_display = ('document_type', 'auto_ocr')


@admin.register(DocumentFileOCRError)
class DocumentFileOCRErrorAdmin(admin.ModelAdmin):
    list_display = ('document_file', 'datetime_submitted')
    readonly_fields = ('document_file', 'datetime_submitted', 'result')

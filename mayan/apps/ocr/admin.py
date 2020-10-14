from django.contrib import admin

from .models import (
    DocumentTypeOCRSettings, DocumentVersionOCRError,
    DocumentVersionPageOCRContent
)


@admin.register(DocumentTypeOCRSettings)
class DocumentTypeOCRSettingsAdmin(admin.ModelAdmin):
    list_display = ('document_type', 'auto_ocr')


@admin.register(DocumentVersionOCRError)
class DocumentVersionOCRErrorAdmin(admin.ModelAdmin):
    list_display = ('document_version', 'datetime_submitted')
    readonly_fields = ('document_version', 'datetime_submitted', 'result')


@admin.register(DocumentVersionPageOCRContent)
class DocumentVersionPageOCRContentAdmin(admin.ModelAdmin):
    list_display = ('document_version_page',)

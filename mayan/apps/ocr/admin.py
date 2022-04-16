from django.contrib import admin

from .models import DocumentTypeOCRSettings, DocumentVersionPageOCRContent


@admin.register(DocumentTypeOCRSettings)
class DocumentTypeOCRSettingsAdmin(admin.ModelAdmin):
    list_display = ('document_type', 'auto_ocr')


@admin.register(DocumentVersionPageOCRContent)
class DocumentVersionPageOCRContentAdmin(admin.ModelAdmin):
    list_display = ('document_version_page',)

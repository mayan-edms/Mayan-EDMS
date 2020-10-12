from django.contrib import admin

from .models import (
    DocumentFilePageContent, DocumentFileParseError
)


@admin.register(DocumentFilePageContent)
class DocumentFilePageContentAdmin(admin.ModelAdmin):
    list_display = ('document_file_page',)


@admin.register(DocumentFileParseError)
class DocumentFileParseErrorAdmin(admin.ModelAdmin):
    list_display = ('document_file', 'datetime_submitted')
    readonly_fields = ('document_file', 'datetime_submitted', 'result')

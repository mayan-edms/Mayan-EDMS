from django.contrib import admin

from .models import (
    DocumentPageContent, DocumentFileParseError
)


@admin.register(DocumentPageContent)
class DocumentPageContentAdmin(admin.ModelAdmin):
    list_display = ('document_page',)


@admin.register(DocumentFileParseError)
class DocumentFileParseErrorAdmin(admin.ModelAdmin):
    list_display = ('document_file', 'datetime_submitted')
    readonly_fields = ('document_file', 'datetime_submitted', 'result')

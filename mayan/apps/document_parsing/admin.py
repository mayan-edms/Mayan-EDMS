from __future__ import unicode_literals

from django.contrib import admin

from .models import (
    DocumentVersionPageContent, DocumentVersionParseError
)


@admin.register(DocumentVersionPageContent)
class DocumentVersionPageContentAdmin(admin.ModelAdmin):
    list_display = ('document_version_page',)


@admin.register(DocumentVersionParseError)
class DocumentVersionParseErrorAdmin(admin.ModelAdmin):
    list_display = ('document_version', 'datetime_submitted')
    readonly_fields = ('document_version', 'datetime_submitted', 'result')

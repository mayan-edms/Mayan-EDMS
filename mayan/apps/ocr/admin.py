from __future__ import unicode_literals

from django.contrib import admin

from .models import DocumentVersionOCRError


class DocumentVersionOCRErrorAdmin(admin.ModelAdmin):
    list_display = ('document_version', 'datetime_submitted')
    readonly_fields = ('document_version', 'datetime_submitted', 'result')


admin.site.register(DocumentVersionOCRError, DocumentVersionOCRErrorAdmin)

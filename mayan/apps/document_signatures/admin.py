from __future__ import unicode_literals

from django.contrib import admin

from .models import DocumentVersionSignature


@admin.register(DocumentVersionSignature)
class DocumentVersionSignatureAdmin(admin.ModelAdmin):
    def document(self, instance):
        return instance.document_version.document

    def has_detached_signature(self, instance):
        return True if instance.signature_file else False

    has_detached_signature.boolean = True
    list_display = (
        'document', 'document_version', 'has_embedded_signature',
        'has_detached_signature'
    )
    list_display_links = ('document_version',)
    search_fields = ('document_version__document__label',)

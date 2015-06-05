from __future__ import unicode_literals

from django.contrib import admin

from .models import DocumentVersionSignature


class DocumentVersionSignatureAdmin(admin.ModelAdmin):
    def has_detached_signature(self, instance):
        return True if instance.signature_file else False

    has_detached_signature.boolean = True
    list_display = ('document_version', 'has_embedded_signature', 'has_detached_signature')
    list_display_links = ('document_version',)


admin.site.register(DocumentVersionSignature, DocumentVersionSignatureAdmin)

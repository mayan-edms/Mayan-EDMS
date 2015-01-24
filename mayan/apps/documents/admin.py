from __future__ import unicode_literals

from django.contrib import admin

from .models import (
    Document, DocumentPage, DocumentPageTransformation, DocumentType,
    DocumentTypeFilename, DocumentVersion, RecentDocument
)


class DocumentPageInline(admin.StackedInline):
    model = DocumentPage
    extra = 1
    classes = ('collapse-open',)
    allow_add = True


class DocumentVersionInline(admin.StackedInline):
    model = DocumentVersion
    extra = 1
    classes = ('collapse-open',)
    allow_add = True


class DocumentTypeFilenameInline(admin.StackedInline):
    model = DocumentTypeFilename
    extra = 1
    classes = ('collapse-open',)
    allow_add = True


class DocumentTypeAdmin(admin.ModelAdmin):
    inlines = [
        DocumentTypeFilenameInline
    ]


class DocumentPageTransformationAdmin(admin.ModelAdmin):
    model = DocumentPageTransformation


class DocumentAdmin(admin.ModelAdmin):
    inlines = [
        DocumentVersionInline
    ]
    list_display = ('uuid', 'label',)


class RecentDocumentAdmin(admin.ModelAdmin):
    model = RecentDocument
    list_display = ('user', 'document', 'datetime_accessed')
    readonly_fields = ('user', 'document', 'datetime_accessed')
    list_filter = ('user',)
    date_hierarchy = 'datetime_accessed'


admin.site.register(Document, DocumentAdmin)
admin.site.register(DocumentPageTransformation,
                    DocumentPageTransformationAdmin)
admin.site.register(DocumentType, DocumentTypeAdmin)
admin.site.register(RecentDocument, RecentDocumentAdmin)

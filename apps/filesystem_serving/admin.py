from django.contrib import admin

from filesystem_serving.models import DocumentMetadataIndex


class DocumentMetadataIndexInline(admin.StackedInline):
    model = DocumentMetadataIndex
    extra = 1
    classes = ('collapse-open',)
    allow_add = True
    readonly_fields = ('suffix', 'metadata_index', 'filename')
